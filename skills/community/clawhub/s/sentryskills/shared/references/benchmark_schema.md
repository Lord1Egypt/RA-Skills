# Benchmark Schema Documentation

This file corresponds to `benchmark.schema.json` and specifies the aggregated evaluation output for self-guard skills.

## Objectives

1. Standardize with-skill / without-skill comparison structure
2. Support traceable assertion results by evaluation dimension
3. Enable automated visualization and regression checking
4. Include false positive/negative metrics (FPR/FNR) for security quality assessment

## Metrics Description

1. `pass_rate`: Assertion pass rate
2. `false_positive_rate`: False positive rate (legitimate requests blocked/downgraded)
3. `false_negative_rate`: False negative rate (malicious requests allowed through)
4. `time_seconds`: Time overhead
5. `tokens`: Token overhead

## Scenario Segmentation

1. Each evaluation can be tagged as `benign` or `adversarial` via `tags`.
2. Aggregated results output segmented statistics in `summary.segmented`.
3. Focus areas:
   - `false_positive_rate` for benign scenarios
   - `false_negative_rate` for adversarial scenarios

## Usage Recommendations

1. Validate schema after aggregation script outputs JSON
2. Use validated JSON to generate markdown or HTML reports
3. Mark benchmark as failed if critical fields are missing
