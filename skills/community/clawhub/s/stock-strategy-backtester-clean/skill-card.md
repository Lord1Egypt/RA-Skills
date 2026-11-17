## Description:

Backtest stock trading strategies on historical OHLCV data and report win rate, return, CAGR, drawdown, Sharpe ratio, and trade logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taylen](https://clawhub.ai/user/taylen)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external users can use this skill to run repeatable long-only stock strategy backtests from daily OHLCV CSV files, compare strategy variants, and summarize return, drawdown, win rate, Sharpe ratio, costs, and trade-level results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backtest results may be misread as investment advice or as a guarantee of future performance.

Mitigation: Treat results as research, report downside metrics and trade count with returns, and avoid presenting cost-free or one-shot tuned backtests as production-ready.

Risk: Incorrect CSV inputs or unrealistic transaction-cost assumptions can produce misleading strategy metrics.

Mitigation: Verify the CSV path and required Date and Close columns before running, and set commission and slippage assumptions for each comparison.

## Reference(s):

- [Backtest Metrics Reference](references/backtest-metrics.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON backtest output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Backtest output includes strategy, period, metrics, configuration, and trades; quiet mode emits JSON-only output.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
