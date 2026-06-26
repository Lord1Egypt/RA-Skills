## Description: <br>
Backtests long-only stock trading strategies against historical OHLCV CSV data and reports performance metrics, transaction-cost assumptions, and trade logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taylen](https://clawhub.ai/user/taylen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to run repeatable stock strategy backtests from selected OHLCV CSV files and summarize return, drawdown, win rate, Sharpe ratio, and trade-level results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtest results can be mistaken for investment advice or future performance guarantees. <br>
Mitigation: Treat outputs as research, report downside metrics and trade count with returns, and validate strategies out of sample before relying on them. <br>
Risk: The bundled Python script reads local CSV files selected by the user. <br>
Mitigation: Run it only on intended market-data files and avoid using sensitive non-market datasets. <br>


## Reference(s): <br>
- [Backtest Metrics Reference](references/backtest-metrics.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/taylen/stock-strategy-backtester-clean) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, JSON] <br>
**Output Format:** [Markdown summaries with shell command examples and JSON backtest results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-selected CSV files and reports strategy configuration, metrics, and trades.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
