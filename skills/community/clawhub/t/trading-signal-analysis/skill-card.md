## Description:

Trading Signal Analysis helps agents analyze stock or cryptocurrency OHLCV data, generate technical buy and sell signals, backtest strategies, and produce risk and performance diagnostics through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading researchers use this skill to submit OHLCV candle data for technical signal detection, strategy backtesting, chart generation, and trade risk analysis. It is suited for evaluating systematic trading ideas and reviewing momentum, drawdown, MAE/MFE, win rate, and expectancy metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated charts and trade logs may be stored in cloud storage by default.

Mitigation: Before use, decide whether OHLCV data, symbols, strategy settings, results, charts, and trade logs can be sent to AgentPMT; for sensitive work, disable chart and trade-log storage or reduce expiration_days.

Risk: The skill documentation includes floating installer examples.

Mitigation: Prefer a pinned and verified install path before production deployment.

Risk: Trading signals and backtests can be incorrect or misleading if inputs, assumptions, or parameters are unsuitable.

Mitigation: Review candle quality, indicator parameters, transaction costs, annualization settings, and returned warnings before using results in a trading workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/trading-signal-analysis)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/trading-signal-analysis)
- [Trading Signal Analysis Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and hosted tool response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses may include signal counts, recent signal events, indicator values, trade logs, equity curves, performance metrics, downloadable PNG charts, and CSV trade logs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
