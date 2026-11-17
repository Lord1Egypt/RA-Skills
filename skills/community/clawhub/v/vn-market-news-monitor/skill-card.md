## Description:

Tracks Vietnam market and sector narratives from major domestic financial media; used when users ask for market stories, sector heat, and most-mentioned Vietnamese tickers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to monitor Vietnamese financial media narratives, rank sector and ticker mention intensity, and flag freshness, source coverage, bias, and validation concerns before any investment action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial headlines and ticker mentions can be mistaken for investment advice.

Mitigation: Treat outputs as media-signal monitoring only, do not issue buy or sell commands, and verify cited headlines and quantitative data before acting.

Risk: Weak source coverage, stale headlines, duplicate stories, or concentration in one publisher can distort narrative rankings.

Mitigation: Report source coverage, collection window in ICT, last update per source, de-duplication status, confidence rating, and the major noise or bias factor.

Risk: Public web pages and search results may be unavailable or incomplete.

Mitigation: Prefer direct source pages, fall back to search results when needed, list inaccessible sources, and downgrade confidence to Low when fewer than three domestic sources are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teahann/skills/vn-market-news-monitor)
- [CafeF](https://cafef.vn/)
- [VnEconomy](https://vneconomy.vn/)
- [VietnamFinance](https://vietnamfinance.vn/)
- [Vietstock](https://vietstock.vn/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with source links, coverage table, freshness window, confidence rating, sector and ticker narrative sections, and validation checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an optional watchlist impact map when the user provides tickers.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
