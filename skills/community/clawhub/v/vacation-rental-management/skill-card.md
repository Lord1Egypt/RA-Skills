## Description:

Manage vacation rental turnovers, guest reservations, and cleaning schedules; auto-schedule cleanings based on guest check-out, coordinate multi-property turnovers, manage checklists, and support CLI, MCP server, and REST API approaches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mchusma](https://clawhub.ai/user/mchusma)

### License/Terms of Use:

MIT-0

## Use Case:

External vacation-rental hosts, short-term rental managers, property operators, and developers use this skill to coordinate guest reservations, turnover cleanings, checklists, property setup, and schedule changes through TIDY CLI, MCP, or REST API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad authority over reservations, jobs, property records, credentials, and access details.

Mitigation: Review the skill before installing it and use it only with a TIDY account and token whose authority is acceptable for the intended properties.

Risk: Agent actions may cancel, reschedule, delete, or bulk-change operational property-management records.

Mitigation: Require explicit human confirmation before cancellations, reschedules, deletes, or bulk changes.

Risk: Property setup and workflow examples may include sensitive gate, parking, or lockbox access details.

Mitigation: Avoid sending permanent gate or lockbox codes unless strictly necessary, and prefer temporary or rotated access instructions where possible.

## Reference(s):

- [Vacation Rental Management ClawHub Page](https://clawhub.ai/mchusma/skills/vacation-rental-management)
- [TIDY Homepage](https://tidy.com)
- [TIDY REST API Docs](https://public-api.tidy.com/docs)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Authentication](references/authentication.md)
- [MCP Server Reference](references/mcp-server-reference.md)
- [REST API Reference](references/rest-api-reference.md)
- [Vacation Rental Workflows](references/vacation-workflows.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with bash, JSON, MCP, and REST API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes TIDY CLI commands, MCP server configuration, REST requests, and async polling guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
