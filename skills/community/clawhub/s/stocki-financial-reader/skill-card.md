## Description: <br>
Institutional-grade financial data skill for OpenClaw. Real-time quotes, financials, valuation time series, OHLCV history, industry membership, consensus forecasts, composite analysis. Covers cn/hk/us markets and stock/index/etf/futures/crypto. For structured market/financial data, use this skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17817942676](https://clawhub.ai/user/17817942676) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw and ClawBot users use this skill to retrieve structured market and financial data through the Stocki gateway, including quotes, OHLCV history, fundamentals, valuation panels, industry membership, market calendars, and consensus data. It is a data retrieval and analysis aid, not an investment advice or transaction execution tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends market-data queries and API-key authenticated requests to the configured Stocki gateway. <br>
Mitigation: Install only when the Stocki service is trusted, keep STOCKI_API_KEY out of source code and chat logs, rotate exposed keys, and avoid sending personal or confidential context in financial queries. <br>
Risk: Optional setup diagnostics contact the configured gateway to verify authentication and reachability. <br>
Mitigation: Run diagnostics only when ready to test the configured gateway and report their exit codes without retrying automatically. <br>
Risk: Returned financial data may be delayed, adjusted upstream, or insufficient for a requested decision. <br>
Mitigation: Relay only data present in real responses, preserve non-advisory wording, and have users verify independently before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/17817942676/stocki-financial-reader) <br>
- [Install and setup](INSTALL.md) <br>
- [Market calendar](references/market-calendar.md) <br>
- [Realtime quote](references/realtime-quote.md) <br>
- [Price history](references/price-history.md) <br>
- [Industry and symbols](references/industry-and-symbols.md) <br>
- [Fundamentals panel](references/fundamentals-panel.md) <br>
- [Consensus and target](references/consensus-and-target.md) <br>
- [Financial context](references/financial-context.md) <br>
- [Metric resolver](references/metric-resolver.md) <br>
- [Name resolver](references/name-resolver.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses with structured market-data summaries and optional bash commands for setup diagnostics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STOCKI_GATEWAY_URL and STOCKI_API_KEY; data returned by the Stocki gateway is governed separately from the MIT-0 skill code.] <br>

## Skill Version(s): <br>
0.4.0 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
