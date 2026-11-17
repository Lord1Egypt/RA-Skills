## Description:

AI-powered operations knowledge management. Search process documentation, capacity plans, resource allocation data, and KPI dashboards with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams and managers use this skill to search organization-specific SOPs, runbooks, incident postmortems, capacity plans, vendor SLAs, KPI definitions, and operational dashboards through UPLO-backed MCP tools. It supports incident response, capacity planning, operational reviews, documentation maintenance, and process improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned third-party npm MCP server with a sensitive UPLO token.

Mitigation: Install only from a trusted package source, use a least-privilege UPLO MCP token, pin or otherwise control the MCP server version where possible, and run it in a restricted environment.

Risk: The skill can expose broad organizational context, including confidential strategic operational plans and cost models.

Mitigation: Respect classification tiers, avoid broad exports or persistent logs unless authorized, and minimize or redact sensitive content before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-operations)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with MCP tool calls, search guidance, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an UPLO MCP token and returns organization-specific operations context according to the connected knowledge base and access controls.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
