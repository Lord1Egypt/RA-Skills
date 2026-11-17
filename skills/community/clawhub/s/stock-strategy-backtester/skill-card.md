## Description:

Backtest stock trading strategies on historical OHLCV CSV data and report returns, CAGR, drawdown, Sharpe ratio, win rate, and trade logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taylen](https://clawhub.ai/user/taylen)

### License/Terms of Use:


## Use Case:

Developers, analysts, and investors use this skill to run local long-only backtests for SMA crossover, RSI reversion, and breakout strategies, compare parameter variants, and summarize risk-adjusted performance from OHLCV CSV data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backtest results may be mistaken for financial advice or future performance guarantees.

Mitigation: Present results as research, include date range, transaction costs, drawdown, and trade count, and state that backtests are not guarantees.

Risk: Broad trigger wording may activate the skill for general return or strategy questions.

Mitigation: Confirm the user wants a local CSV-based backtest before running commands or interpreting results.

Risk: Poor data quality or one-shot parameter tuning can produce misleading strategy performance.

Mitigation: Validate required Date and Close columns, compare variants on the same date range and cost model, and prefer walk-forward or out-of-sample checks.

## Reference(s):

- [Backtest Metrics Reference](references/backtest-metrics.md)
- [ClawHub Skill Page](https://clawhub.ai/taylen/skills/stock-strategy-backtester)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON backtest result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local CSV inputs and reports strategy period, metrics, configuration, and trades.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
