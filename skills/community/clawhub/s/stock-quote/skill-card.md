## Description:

Fetches stock prices and selected fundamental data for one or more stock symbols using Stooq, yfinance, Financial Modeling Prep, or Yahoo Finance pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to look up stock quotes, refresh portfolio valuations, and check basic price or fundamental signals before analysis or trading-rule checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a daily heartbeat example that can cause agents to write recurring portfolio-memory updates with hard-coded holdings and a stop-loss value that may not belong to the user.

Mitigation: Do not add HEARTBEAT.md or MEMORY.md entries unless the holdings, share counts, stop-losses, recurrence, and deletion path are explicitly provided and approved by the user.

Risk: Quote data may be delayed or incomplete, especially because the default Stooq source is described as delayed end-of-day data.

Mitigation: Treat quote data as informational and verify prices with an authoritative market data source before trading or financial decisions.

Risk: The skill depends on network data sources and optional Python packages.

Mitigation: Install dependencies in an isolated, pinned environment for higher assurance.

## Reference(s):

- [Stock Data API Sources](references/api-sources.md)
- [Stooq quote CSV endpoint](https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlc&h=&t=csv)
- [Yahoo Finance quote pages](https://finance.yahoo.com/quote/{SYMBOL})
- [Financial Modeling Prep](https://financialmodelingprep.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Code]

**Output Format:** [Human-readable quote text or JSON objects from the quote CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote records may include price, change, previous close, day range, volume, market capitalization, P/E ratio, 52-week range, dividend yield, timestamp, source, or error fields depending on the data source.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
