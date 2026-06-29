## Description: <br>
Trading Signal Analysis helps agents analyze OHLCV market data, generate technical trading signals, run strategy backtests, and produce risk and performance diagnostics through AgentPMT-hosted tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and trading workflow builders use this skill to submit stock or cryptocurrency candle data for signal detection, strategy backtests, and MAE/MFE risk diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends candle data, symbols, strategy settings, and generated analysis to AgentPMT-hosted services. <br>
Mitigation: Use only data approved for AgentPMT, minimize inputs, and avoid sending proprietary or confidential trading data unless that sharing is acceptable. <br>
Risk: Generated charts and trade logs can contain market data and strategy results in downloadable artifacts. <br>
Mitigation: Set store_charts and store_trade_log to false when files are not needed, and use the shortest practical expiration_days setting for retained artifacts. <br>


## Reference(s): <br>
- [AgentPMT Trading Signal Analysis marketplace page](https://www.agentpmt.com/marketplace/trading-signal-analysis) <br>
- [ClawHub Trading Signal Analysis listing](https://clawhub.ai/agentpmt/skills/trading-signal-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON request examples; remote tool responses are JSON and may include signed download links for PNG charts and CSV trade logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least 30 OHLCV candles; optional parameters control indicators, strategy choice, risk controls, chart generation, and artifact retention.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
