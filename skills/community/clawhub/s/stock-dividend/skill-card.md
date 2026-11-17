## Description:

Analyze dividend metrics for stocks via AIsa API, including yield, payout ratio, growth CAGR, safety score, income rating, and Dividend Aristocrat/King status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request dividend income analysis for one or more stock tickers, including safety scoring, payout analysis, growth metrics, and ranked comparisons. The reports are informational and should be verified before making financial decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the required AIsa API key to a custom endpoint if AISA_BASE_URL is set.

Mitigation: Set AISA_BASE_URL only to an endpoint you control and trust, or leave it unset to use the default AIsa endpoint.

Risk: Dividend reports may contain incorrect or incomplete financial data or analysis.

Mitigation: Treat generated reports as informational and verify financial data independently before acting on it.

## Reference(s):

- [ClawHub Stock Dividend listing](https://clawhub.ai/bibaofeng/skills/stock-dividend)
- [AIsa homepage](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown dividend analysis report with tables and an optional JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; optional AISA_BASE_URL and AISA_MODEL change the API endpoint and model used.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
