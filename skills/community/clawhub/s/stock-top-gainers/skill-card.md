## Description:

Gets the top 20 China A-share stocks by 10-trading-day gain and filters out ST-designated stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinelp100](https://clawhub.ai/user/shinelp100)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to retrieve a ranked, filtered snapshot of recent China A-share market gainers for informational market review. The output is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data may be delayed, stale, or sourced from a bundled cached sample when live browsing fails.

Mitigation: Treat the output as informational only and verify time-sensitive prices or rankings against an authoritative market data source before use.

Risk: The skill browses third-party financial websites to obtain public market data.

Mitigation: Review site terms, network access expectations, and browser tool permissions before deployment.

Risk: Financial ranking output could be mistaken for investment advice.

Mitigation: Present results with the documented informational-use disclaimer and avoid using the skill as the sole basis for trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinelp100/skills/stock-top-gainers)
- [Tonghuashun iWencai query](https://www.iwencai.com/unifiedwap/result?w=%E8%BF%91%2010%20%E6%97%A5%E6%B6%A8%E5%B9%85%E6%8E%92%E5%90%8D)
- [Eastmoney margin financing data](https://data.eastmoney.com/rzrq/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown table or JSON list of ranked stock records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes rank, stock code, stock name, closing price, 10-day gain, daily change, and sometimes industry or ranking metadata.]

## Skill Version(s):

1.0.2 (source: release evidence, README changelog, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
