## Description:

Calculates China A-share technical indicators, volume-price patterns, resonance signals, backtests, position sizing, risk analysis, market sentiment, and LSTM price forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbabyzs](https://clawhub.ai/user/gbabyzs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-analysis agents use this skill to calculate technical indicators, identify multi-indicator trading signals, evaluate position sizing and risk metrics, run backtests, and produce informational stock-analysis outputs for China A-share workflows.

### Deployment Geography for Use:

Global, with current market-data examples and calculations focused on China A-share equities.

## Known Risks and Mitigations:

Risk: Loading untrusted model or scaler files can execute code through the pickle scaler loader.

Mitigation: Use only model and scaler artifacts generated or reviewed by a trusted source, run the skill in an isolated virtual environment, and avoid third-party .pkl files.

Risk: Trading signals, forecasts, target prices, stop losses, and position sizes may be mistaken for automated trading authority.

Mitigation: Treat outputs as informational analysis, validate them against current market data, and require independent human judgment before any trading action.

Risk: Market-data quality, dependency behavior, or delayed quotes can affect calculated indicators and backtest conclusions.

Mitigation: Pin and review dependencies, confirm data-source freshness, and rerun tests or backtests with representative data before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gbabyzs/skills/technical-indicators)
- [Technical indicators skill guide](artifact/SKILL.md)
- [Position sizing and risk README](artifact/README.md)
- [LSTM predictor README](artifact/README_LSTM.md)
- [Market sentiment README](artifact/README_MARKET_SENTIMENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON-style analysis outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include indicator values, signal strength scores, buy/sell-style recommendations, backtest metrics, position-size estimates, and forecast JSON; all financial outputs are informational.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
