"""
Decision engine for MSSD volatility detection

Author: Celia Mercier
"""

import pandas as pd
import os


def calculate_mssd(df, window=3):
    df = df.copy()
    df = df.sort_values(["user_id", "timestamp"])

    df["ema_diff_squared"] = df.groupby("user_id")["ema"].diff() ** 2

    df["observed_mssd"] = (
        df.groupby("user_id")["ema_diff_squared"]
        .rolling(window=window, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    return df


def apply_decision_rules(df, threshold_quantile=0.80, cooldown_minutes=5, max_prompts_per_day=4):
    df = df.copy()
    df = df.sort_values(["user_id", "timestamp"])

    df["send_prompt"] = False
    df["decision_reason"] = "below threshold"

    threshold = df["observed_mssd"].quantile(threshold_quantile)

    for user_id in df["user_id"].unique():
        user_df = df[df["user_id"] == user_id]

        last_prompt_time = None
        prompts_by_day = {}

        for idx, row in user_df.iterrows():
            if pd.isna(row["observed_mssd"]):
                df.at[idx, "decision_reason"] = "missing or insufficient EMA data"

            elif row["observed_mssd"] < threshold:
                df.at[idx, "decision_reason"] = "below threshold"

            else:
                day = row["timestamp"].date()

                if day not in prompts_by_day:
                    prompts_by_day[day] = 0

                if prompts_by_day[day] >= max_prompts_per_day:
                    df.at[idx, "decision_reason"] = "daily cap reached"

                elif last_prompt_time is not None and (
                    row["timestamp"] - last_prompt_time
                ).total_seconds() / 60 < cooldown_minutes:
                    df.at[idx, "decision_reason"] = "cooldown active"

                else:
                    df.at[idx, "send_prompt"] = True
                    df.at[idx, "decision_reason"] = "prompt sent"
                    last_prompt_time = row["timestamp"]
                    prompts_by_day[day] += 1

    return df


def summarize_decisions(df):
    summary = df.groupby("user_id").agg(
        prompts_sent=("send_prompt", "sum"),
        average_mssd=("observed_mssd", "mean"),
        max_mssd=("observed_mssd", "max"),
    )

    return summary.reset_index()