## Description:

OpenClaw stock analysis skill for US/HK/CN markets. Combines QVeris data sources (THS, Caidazi, Alpha Vantage, Finnhub, X sentiment) for quote, fundamentals, technicals, news radar, morning/evening brief, and actionable investment insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buxibuxi](https://clawhub.ai/user/buxibuxi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to analyze US, Hong Kong, and China equities, compare symbols, manage watchlists, and generate market briefs or radar from QVeris-powered data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends stock symbols, watchlist context, and analysis queries to QVeris using QVERIS_API_KEY.

Mitigation: Install only when this data sharing is acceptable, keep the API key scoped for read-only use, and avoid placing secrets in prompts, logs, or configuration files.

Risk: Auto-invocation and optional cron jobs can create recurring QVeris API usage.

Mitigation: Review auto-invocation before enabling the skill and add scheduled jobs only when recurring market briefs or radar runs are intended.

Risk: The skill stores local watchlist state and optional tool-template evolution state inside the skill directory.

Mitigation: Review watchlist contents before use and run with --no-evolution when local tool-template state should not be persisted.

Risk: Stock analysis outputs can be incomplete, stale, or unsuitable as investment advice.

Mitigation: Treat outputs as research support, check source freshness and consistency, and verify decisions against independent financial analysis.

## Reference(s):

- [Stock Copilot Pro on ClawHub](https://clawhub.ai/buxibuxi/skills/stock-copilot-pro)
- [QVeris](https://qveris.ai)
- [Metrics and Signals](references/metrics-and-signals.md)
- [Report Template](references/report-template.md)
- [Tool Selection Strategy](references/tool-selection.md)
- [Sector Benchmarks](references/sector-benchmarks.json)
- [Tool Chains](references/tool-chains.json)
- [OpenClaw Cron Example](config/openclaw-cron.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, or chat-friendly text with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include concise research reports, comparison summaries, watchlist updates, scheduled brief guidance, and optional evidence traces.]

## Skill Version(s):

0.3.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
