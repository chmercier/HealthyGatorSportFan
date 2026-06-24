# REACT Volatility Detection Simulator

Author: Celia Mercier

## Overview

This module extends the existing code from Tyler going into MSSD.
The implementation is designed to operate ENTIRELY on synthetic data

---

# Files

## decision_engine.py

Core volatility detection logic.

### Features

#### MSSD Calculation

Calculates observed Mean Square Successive Difference (MSSD) from sequential EMA responses.

MSSD is a commonly used within-person volatility metric that measures how much an individual's responses fluctuate over time.

Outputs:

- observed_mssd
- squared EMA differences

#### Decision Rules

Implements intervention delivery logic:

- Volatility threshold detection
- Cooldown enforcement
- Daily prompt limits
- Decision logging

Outputs:

- send_prompt
- decision_reason

#### Summary Statistics

Generates participant-level summaries including:

- Total prompts sent
- Average MSSD
- Maximum observed MSSD

---

## run_decision_engine.py

Standalone execution script.

### Workflow

1. Generates synthetic EMA data using the existing cohort generator.
2. Calculates observed MSSD values.
3. Applies intervention decision rules.
4. Generates summary statistics.
5. Exports results to CSV files.

Output files:

- outputs/decision_log.csv
- outputs/decision_summary.csv

---

# Outputs

## decision_log.csv

Participant-level event log containing:

| Column | Description |
|----------|-------------|
| user_id | Synthetic participant ID |
| timestamp | EMA timestamp |
| ema | EMA response value |
| observed_mssd | Calculated volatility score |
| send_prompt | Whether an intervention was triggered |
| decision_reason | Explanation for decision |

---

## decision_summary.csv

Participant-level summary statistics.

| Column | Description |
|----------|-------------|
| user_id | Synthetic participant ID |
| prompts_sent | Number of prompts delivered |
| average_mssd | Mean volatility level |
| max_mssd | Highest observed volatility |

---

# Requirements Mapping

## Requirement 1: Define Synthetic Scenarios

### Low Volatility

Characteristics:

- Stable EMA responses
- Small response changes
- Low MSSD values

Expected Result:

- Few or no intervention prompts

### High Volatility

Characteristics:

- Rapid EMA fluctuations
- Large response changes
- Elevated MSSD values

Expected Result:

- Intervention prompts triggered
- Cooldown and prompt caps enforced

### Missing Data

Characteristics:

- Missing EMA responses generated through clustered missingness simulation

Current Support:

- Existing synthetic generator produces realistic missing response patterns
- MSSD calculations safely handle missing observations

Expected Result:

- System continues operating without failure
- Missing observations excluded from volatility calculations

### Future Scenario: Late Responses

Planned Extension:

- EMA completion delays
- Response timing compliance analysis
- Prompt effectiveness relative to response latency

---

## Requirement 2: Simulator Skeleton Code

Current Architecture

Synthetic Data Generator
↓
EMA Response Stream
↓
MSSD Calculation
↓
Volatility Threshold Detection
↓
Decision Engine
↓
Prompt Delivery Logic
↓
Decision Log

Primary Components:

- Synthetic cohort generation
- Volatility calculation
- Decision logic
- Result summarization

The implementation is modular and separates data generation from decision-making logic to support future expansion.

---

## Requirement 3: Test Scenarios

### Scenario A: Low Volatility User

Input:

Stable EMA responses.

Expected Output:

- Low MSSD values
- No prompt delivery

Purpose:

Verify false positives remain low.

---

### Scenario B: High Volatility User

Input:

Rapidly changing EMA responses.

Expected Output:

- High MSSD values
- Prompt delivery events generated

Purpose:

Verify volatility detection functions correctly.

---

### Scenario C: Missing Data User

Input:

EMA series containing missing observations.

Expected Output:

- Successful execution
- No system failure
- Volatility calculations continue where possible

Purpose:

Verify robustness to incomplete participant data.

# Summary

This prototype successfully demonstrates a complete synthetic volatility detection pipeline. The system generates synthetic participants, calculates MSSD-based volatility measures, applies intervention decision rules, and produces interpretable outputs for evaluation and future development.