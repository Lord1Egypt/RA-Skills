## Description: <br>
OpenClaw stock analysis skill for US/HK/CN markets. Combines QVeris data sources (THS, Caidazi, Alpha Vantage, Finnhub, X sentiment) for quote, fundamentals, technicals, news radar, morning/evening brief, and actionable investment insights. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[buxibuxi](https://clawhub.ai/user/buxibuxi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to analyze US, Hong Kong, and China equities, compare symbols, manage watchlists, generate daily briefs, and scan market themes using QVeris-sourced market, fundamentals, technical, news, and sentiment data. Outputs are for research and education, not financial or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a QVeris API key and sends stock symbols or watchlist-related queries to qveris.ai. <br>
Mitigation: Use a scoped QVeris API key and install only when that data sharing is acceptable. <br>
Risk: The skill stores local watchlist and parameter-template state. <br>
Mitigation: Review or delete local watchlist and evolution files when needed, and disable evolution for runs that should not update local state. <br>
Risk: Generated stock analysis may be incomplete, stale, or misleading if source data is sparse or provider coverage varies. <br>
Mitigation: Treat output as research rather than financial advice and verify important decisions against authoritative market data. <br>
Risk: Optional scheduled jobs can repeatedly send holdings-oriented prompts through the configured agent workflow. <br>
Mitigation: Review cron job payloads and delivery targets before enabling scheduled briefs or radar runs. <br>


## Reference(s): <br>
- [QVeris](https://qveris.ai) <br>
- [Metrics and Signals](references/metrics-and-signals.md) <br>
- [Report Template](references/report-template.md) <br>
- [Tool Selection Strategy](references/tool-selection.md) <br>
- [Tool Chains](references/tool-chains.json) <br>
- [Sector Benchmarks](references/sector-benchmarks.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance, configuration] <br>
**Output Format:** [Markdown, JSON, or chat-friendly text, depending on command options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include watchlist updates, scheduled brief configuration, source disclosures, and optional evidence traces.] <br>

## Skill Version(s): <br>
0.3.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
