## Description:

Fetch recent finance news headlines for stock, ETF, and index symbols via Yahoo Finance (yfinance), with caching and structured JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phonphrm](https://clawhub.ai/user/phonphrm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-focused users use this skill to fetch recent Yahoo Finance headlines for stocks, ETFs, and indices, then summarize dated headlines with source links. It is intended for informational news checks, not trading advice or complete real-time market coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The yfinance dependency and Yahoo Finance data path are best-effort and may provide stale, incomplete, unavailable, or rate-limited headline data.

Mitigation: Use the skill for informational finance-symbol news checks only, mention Yahoo/yfinance limitations in summaries, and retry with lower frequency or a longer cache TTL when provider errors occur.

Risk: Market headlines can be misread as investment recommendations.

Mitigation: Present headlines, publishers, publication times, and URLs without trading advice phrasing.

Risk: Installing an unpinned dependency may introduce supply-chain variance over time.

Mitigation: Install in an isolated virtual environment and consider pinning yfinance to a reviewed version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phonphrm/skills/yahoofinance-news)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with linked headline details, backed by structured JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes symbol, source, fetched time, item count, headline items, publisher, publication time, URL or link, and summaries when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
