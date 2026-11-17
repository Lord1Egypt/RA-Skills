## Description:

Research ecommerce categories on Reddit to identify buyer pain points, underserved product gaps, trending products, and quote-backed market signals using semantic search via the Reddit Insights MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gityu2016](https://clawhub.ai/user/gityu2016)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, product researchers, and market analysts use this skill to search Reddit discussions, cluster complaints and recommendations, and produce Chinese market research tables with English source quotes. It is suited for validating product ideas, finding recurring customer pain points, and identifying trending products from user discussions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party MCP package with an API key.

Mitigation: Pin reddit-insights-mcp to a reviewed exact version, verify the package source before installation, and run the MCP server with limited privileges.

Risk: Queries and API credentials are sent to an external Reddit search service.

Mitigation: Use a dedicated revocable Reddit Insights API key and avoid sending sensitive health, financial, personal, or confidential business queries unless external sharing is acceptable.

## Reference(s):

- [Reddit Insights](https://reddit-insights.com)
- [ClawHub Skill Page](https://clawhub.ai/gityu2016/skills/reddit-market-insights)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables with source links, quoted evidence, setup configuration snippets, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese analysis fields with English evidence quotes and Reddit post URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
