## Description: <br>
Backtest stock trading strategies on historical OHLCV data and report win rate, return, CAGR, drawdown, Sharpe ratio, and trade logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taylen](https://clawhub.ai/user/taylen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and analysts use this skill to run repeatable long-only stock strategy backtests from OHLCV CSV files, compare SMA crossover, RSI reversion, and breakout rules, and summarize performance with return, drawdown, Sharpe ratio, win rate, and trade logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtest output may be mistaken for financial advice or a reliable prediction of future performance. <br>
Mitigation: Treat results as research support, include drawdown, trade count, transaction costs, and assumptions in summaries, and avoid framing results as investment advice. <br>
Risk: The skill reads local market-price CSV files selected by the user. <br>
Mitigation: Run it only on CSV files intended for analysis and review input paths before execution. <br>


## Reference(s): <br>
- [Backtest Metrics Reference](references/backtest-metrics.md) <br>
- [ClawHub skill page](https://clawhub.ai/taylen/stock-strategy-backtester) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON backtest results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided OHLCV CSV files and prints performance metrics, configuration, and trades.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
