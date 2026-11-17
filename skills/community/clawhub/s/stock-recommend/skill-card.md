## Description:

Analyzes recent international news to identify A-share, Hong Kong, or U.S. stocks that may see unusual price movement, with reasons and news links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violin](https://clawhub.ai/user/violin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers can request a news-based market scan for A-shares, Hong Kong stocks, or U.S. stocks. The skill produces a structured informational report with key headlines, likely bullish or risk-sensitive movers, reasons, and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-movement predictions can be wrong or stale if public news is incomplete, outdated, or misinterpreted.

Mitigation: Use the report as informational analysis only, verify cited links and current market conditions, and do not treat outputs as financial advice.

Risk: The skill relies on recent public web searches, so link quality and publication recency may vary.

Mitigation: Prefer authoritative news sources, check publication timestamps, and validate the cited evidence before acting on the analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/violin/skills/stock-recommend)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with news summary, stock-movement tables, source links, and investment notes]

**Output Parameters:** [1D; market parameter accepts A股, 港股, or 美股]

**Other Properties Related to Output:** [Requires current public-news search; informational only and not investment advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
