## Description:

Analyze read-only dividend metrics for stocks via AIsa API, including yield, payout ratio, growth CAGR, safety score, income rating, and Dividend Aristocrat/King status without placing trades, making purchases, or managing brokerage accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and developers use this skill to request read-only dividend research for one or more stock tickers. It returns dividend metrics, safety scoring, income ratings, status checks, and optional structured JSON without brokerage or order-placement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AISA_API_KEY can be sent to any HTTPS endpoint configured through AISA_BASE_URL.

Mitigation: Use the default AIsa endpoint or set AISA_BASE_URL only to a fully trusted AIsa-compatible HTTPS host.

Risk: Requested tickers and generated analysis prompts are sent to AIsa.

Mitigation: Install only when this data sharing is acceptable for the intended workflow.

Risk: Users may mistake dividend analysis for trading or investment advice.

Mitigation: Keep the workflow read-only, do not provide brokerage credentials or payment details, and treat outputs as informational rather than financial advice.

## Reference(s):

- [Stock Dividend AIsa on ClawHub](https://clawhub.ai/baofeng-tech/skills/stock-dividend-aisa)
- [AIsa Homepage](https://aisa.one)
- [AIsa API Endpoint](https://api.aisa.one/v1)

## Skill Output:

**Output Type(s):** [text, markdown, json]

**Output Format:** [Markdown dividend analysis by default, or JSON when requested with --output json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one or more validated stock ticker symbols and requires AISA_API_KEY.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
