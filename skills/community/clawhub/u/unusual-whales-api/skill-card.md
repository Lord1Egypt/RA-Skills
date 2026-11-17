## Description:

Query the Unusual Whales API for unusual options flow, dark pool prints, market tide, stock greek exposure, financial statements, and technical indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonofbaal](https://clawhub.ai/user/sonofbaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-data users use this skill to select authenticated Unusual Whales API queries for options activity, dark pool trades, market sentiment, company financials, and technical indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is sent to an external service to retrieve market data.

Mitigation: Provide UW_API_KEY only if you intend to use Unusual Whales, and send requests only to api.unusualwhales.com over HTTPS.

Risk: The optional local MCP installation can run a mutable package version.

Mitigation: Prefer the documented GET API path; if using local MCP, verify the package source and pin a trusted version.

## Reference(s):

- [Unusual Whales API documentation](https://api.unusualwhales.com/docs)
- [Unusual Whales API token dashboard](https://unusualwhales.com/dashboard/api)
- [Unusual Whales MCP setup guide](https://unusualwhales.com/public-api/mcp)
- [ClawHub skill listing](https://clawhub.ai/sonofbaal/skills/unusual-whales-api)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown with API request examples and data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API requests require a user-provided UW_API_KEY.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
