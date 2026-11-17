## Description:

Read-only US stock market data API for AI agents, covering prices, sentiment, insider and institutional activity, options, analyst ratings, earnings, and market insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use SentiSense to retrieve US stock prices and market research data, including sentiment, reported trades, institutional holdings, options activity, analyst views, and earnings information. The API is read-only and its output is informational, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags credential provisioning and an unpinned CLI setup for review; scan coverage was partial.

Mitigation: Review the setup before use, consider whether the credential-provisioning step is appropriate, and inspect and pin the CLI version before running it.

## Reference(s):

- [SentiSense API documentation](https://sentisense.ai/docs/api/)
- [SentiSense website](https://sentisense.ai)
- [ClawHub skill page](https://clawhub.ai/thesentitrader/skills/sentisense)

## Skill Output:

**Output Type(s):** [API calls, JSON, Analysis, Guidance]

**Output Format:** [JSON market data with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only informational data; endpoint coverage and detail vary by ticker and subscription tier.]

## Skill Version(s):

2.31.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
