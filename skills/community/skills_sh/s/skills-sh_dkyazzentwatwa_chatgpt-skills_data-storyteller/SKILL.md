---
name: data-storyteller
description: Analyze datasets and turn them into narrative reports with charts, audits, comparisons, and statistical summaries. Use for exploratory analysis and executive-ready outputs.
---

# Data Storyteller

Use this as the primary analytics skill for structured data. It now absorbs the repo's audit, comparison, statistics, pivot, experiment, and time-series helpers.

## Use This For

- Executive summaries and narrative reports from CSV or spreadsheet data
- Data quality audits, comparisons, and anomaly reviews
- Statistical analysis, pivots, experiment reads, ROI and budget analysis
- Survey summaries and time-series decomposition

## Workflow

1. Profile the dataset shape, column types, and missing-value risk.
2. Pick the smallest useful analysis path instead of running every script by default.
3. Start with `scripts/data_storyteller.py` when the user wants a cohesive report.
4. Reach for focused helpers when the task is narrow:
   - `data_quality_auditor.py`
   - `dataset_comparer.py`
   - `correlation_explorer.py`
   - `outlier_detective.py`
   - `statistical_analyzer.py`
   - `survey_analyzer.py`
   - `ts_decomposer.py`
   - `pivot_table_generator.py`
   - `ab_test_calc.py`
   - `roi_calculator.py`
   - `budget_analyzer.py`
5. Translate outputs into plain-English findings, risks, and next actions.

## Guardrails

- Do not overstate causal claims from correlations.
- Call out data quality problems before presenting strong conclusions.
- Keep executive summaries short and move method detail behind them.
