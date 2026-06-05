"""
Run the decision engine without editing existing files
"""
import os
from synthetic_generator import generate_user_ids, generate_cohort
from decision_engine import calculate_mssd, apply_decision_rules, summarize_decisions


if __name__ == "__main__":
    USERS = 100
    DAYS = 7
    EMA_PER_DAY = 5
    RESP_RATE = 0.80
    SEED = 42

    user_ids = generate_user_ids(USERS)

    ema_df = generate_cohort(
        users=USERS,
        days=DAYS,
        ema_per_day=EMA_PER_DAY,
        seed=SEED,
        resp_rate=RESP_RATE,
        user_ids=user_ids,
    )

    decision_df = calculate_mssd(ema_df, window=3)

    decision_df = apply_decision_rules(
        decision_df,
        threshold_quantile=0.80,
        cooldown_minutes=5,
        max_prompts_per_day=4,
    )

    summary_df = summarize_decisions(decision_df)

    decision_df.to_csv(
    os.path.join("syntheticData", "outputs", "decision_log.csv"),
    index=False
)

    summary_df.to_csv(
        os.path.join("syntheticData", "outputs", "decision_summary.csv"),
        index=False
    )
    print(decision_df[[
        "user_id",
        "timestamp",
        "ema",
        "observed_mssd",
        "send_prompt",
        "decision_reason"
    ]].head(30))

    print(summary_df.head())

    print("DONE RUNNING DECISION ENGINE")