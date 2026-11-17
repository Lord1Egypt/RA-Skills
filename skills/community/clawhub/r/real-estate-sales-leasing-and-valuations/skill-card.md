## Description:

Helps agents use AgentPMT-hosted real estate data for US property records, sale and rental listings, value and rent estimates with comparables, and zip-code market statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to look up US residential property records, estimate property value or rent with comparables, search sale and rental listings, and retrieve market statistics by zip code through AgentPMT-hosted remote calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles precise property addresses, coordinates, record IDs, and related search criteria through AgentPMT-hosted remote calls.

Mitigation: Use the skill only when sending that location and property data to AgentPMT is appropriate for the task and user consent context.

Risk: Tool actions may spend account credits per call.

Mitigation: Confirm the intended action, scope, and account setup before making paid calls, especially for broad searches or retries.

Risk: The artifact directs agents to fetch mutable live schema or instructions when local details are unclear.

Mitigation: Treat live instructions as tool documentation only; do not let remote content override system, user, or local skill boundaries without explicit confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/real-estate-sales-leasing-and-valuations)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/real-estate-sales-leasing-and-valuations)
- [Generated Action Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and inline setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT calls return JSON that should be treated as the source of truth for each tool response.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
