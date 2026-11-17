## Description:

Ahrefs API analyst (extension). Reads referring domains, backlinks, organic keywords, and content explorer data via the tested @ahrefs/mcp@0.0.11 server. Pairs with seo-backlinks for multi-source confidence weighting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO analysts, and marketing operations teams use this skill to query live Ahrefs metrics, backlink data, organic keyword data, and content explorer results through an Ahrefs MCP server. It supports multi-source SEO analysis by coordinating Ahrefs results with related SEO skills when overlap or confidence weighting is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external Ahrefs MCP package and install script.

Mitigation: Before installation or version changes, confirm the referenced Ahrefs MCP package and install script come from the expected source.

Risk: Ahrefs API calls may consume metered credits, especially for batch analysis.

Mitigation: Estimate cost before large batches, surface the estimate to the orchestrator, and log actual cost after calls.

Risk: The skill requires an Ahrefs API token and connected MCP tools for live data retrieval.

Mitigation: Verify the Ahrefs MCP connection before calling tools and tell the user when the extension is unavailable.

## Reference(s):

- [Ahrefs API](https://ahrefs.com/api)
- [ClawHub seo-ahrefs skill page](https://clawhub.ai/asale-ai/skills/seo-ahrefs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with cited Ahrefs metrics and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live Ahrefs MCP/API data when the extension and API token are available; Ahrefs usage may consume metered credits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
