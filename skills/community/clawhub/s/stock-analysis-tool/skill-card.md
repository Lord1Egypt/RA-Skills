## Description:

Professional stock and fund technical analysis tool for A-share, Hong Kong, and US markets, including MA, MACD, RSI, KDJ, Bollinger Bands, ATR, volume analysis, and a quantitative scoring system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[write31bug](https://clawhub.ai/user/write31bug)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run command-line technical analysis for stocks, funds, ETFs, and LOFs across A-share, Hong Kong, and US markets. It supports single-security analysis, batch analysis, watchlists, JSON output, terminal tables, and offline test mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live analysis sends requested securities to external market-data providers.

Mitigation: Use --test for offline analysis when live data is not needed, and review data-source behavior before analyzing sensitive watchlists.

Risk: Watchlist entries are saved locally under ~/.stock-analysis/config.json.

Mitigation: Avoid storing sensitive portfolios on shared machines, and review or remove saved watchlist entries when they are no longer needed.

Risk: Technical indicators and quantitative scores can be mistaken for investment advice.

Mitigation: Treat outputs as technical-analysis reference material only and verify decisions with authoritative financial sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/write31bug/skills/stock-analysis-tool)
- [Project Homepage](https://github.com/write31bug/stock-technical-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal table, JSON, ASCII text, or file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-security, batch, watchlist, and offline test modes.]

## Skill Version(s):

1.8.1 (source: server release metadata; artifact _meta.json and script report 1.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
