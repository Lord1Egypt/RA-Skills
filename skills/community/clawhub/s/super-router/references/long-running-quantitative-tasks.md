# Long-Running Quantitative Tasks with Super-Router

## When to Use Background Mode
- Any task involving Monte Carlo simulation, GBM modeling, or heavy statistical computation will exceed the 600s foreground timeout.
- Always launch with `background=true` + `notify_on_complete=true` for these workloads.
- Foreground `--stream` runs are limited to 600s and will be killed.

## Prompt Engineering for Numeric/Price Inputs
- Explicitly write the number in words or with clear units: "exactly 212 dollars" instead of "~$212".
- List target price levels explicitly in the prompt (e.g., 220, 240, 260, 280, 300) to reduce hallucination risk.
- The router has shown a tendency to misparse "$212" as much lower values or drop the price context entirely during complex modeling steps.

## Observed Failure Modes
- Price level hallucination during Monte Carlo / GBM steps (common when the model receives ambiguous numeric input).
- Timeout during Step 5 (Monte Carlo simulation) even when volatility modeling is requested.
- Finalizer sometimes produces reports based on completely wrong price assumptions if the prompt is not extremely explicit.

## Recommended Workflow
1. First attempt: background mode with very explicit numeric phrasing.
2. If the first run produces wrong price levels in the output, immediately start a second background job with even more rigid prompt language.
3. Never rely on a single router run for financial probability estimates without verifying the price context in the final report.
