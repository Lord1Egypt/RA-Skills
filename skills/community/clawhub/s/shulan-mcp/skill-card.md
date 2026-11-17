## Description:

Shulan MCP helps agents create, track, browse, and retrieve ShuLan business data research reports for market data, KOL lists, bidding summaries, company insights, recruiting signals, and public-opinion trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shulan-io](https://clawhub.ai/user/shulan-io)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to connect an MCP client to the ShuLan data platform, create business research tasks, monitor task status, and retrieve generated reports for decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send research prompts, business context, and an API key to a configurable ShuLan service endpoint.

Mitigation: Use only a trusted HTTPS ShuLan endpoint and keep the API key out of shared or committed configuration files.

Risk: The skill can create billable one-off or subscription research tasks without an inherent confirmation safeguard.

Mitigation: Require explicit user approval before each shulan_create_task call, especially for subscription tasks or sensitive business and customer data.

Risk: Generated research reports may contain incomplete, outdated, or source-dependent findings.

Mitigation: Review the report's cited source evidence and communicate uncertainty before using results for business decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shulan-io/skills/shulan-mcp)
- [MCP Integration Guide](docs/mcp.md)
- [ShuLan Website](https://shulan.io)
- [npm Package](https://www.npmjs.com/package/shulan-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown guidance with JSON MCP tool responses and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ShuLan API key and may create billable one-off or subscription research tasks.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
