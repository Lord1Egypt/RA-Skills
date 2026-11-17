## Description:

Fetch comprehensive stock data from Simplywall.st. Use when user asks about stock prices, valuation, financials, dividend, or investment analysis for any global stock.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raufimusaddiq](https://clawhub.ai/user/raufimusaddiq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch public SimplyWall.st stock data for ticker-level price, valuation, financial, dividend, forecast, insider activity, and investment-analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker and exchange lookups are sent to SimplyWall.st.

Mitigation: Use the skill only when sending those lookup terms to SimplyWall.st is acceptable.

Risk: Returned stock data is third-party financial data and may be incomplete, delayed, or unsuitable as investment advice.

Mitigation: Treat results as informational context and verify material decisions against authoritative market data, filings, or qualified financial review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raufimusaddiq/skills/stock-data-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/raufimusaddiq)
- [SimplyWall.st](https://simplywall.st)

## Skill Output:

**Output Type(s):** [JSON, text]

**Output Format:** [Structured JSON object with success status, stock data fields, source URL, and error text when retrieval fails.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ticker parameter; exchange is optional and defaults to IDX. Data is fetched from public SimplyWall.st pages.]

## Skill Version(s):

2.0.0 (source: SKILL.md metadata.openclaw.version, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
