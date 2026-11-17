## Description:

Decide which AI agent tool calls need human approval in withHuman, and who approves them, by writing approval pipelines and escalation paths through the withHuman MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[withhuman](https://clawhub.ai/user/withhuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure and manage human approval rules for agent tool calls in withHuman, including reviewers, escalation paths, previews, and revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect approval rules could allow or block agent actions unexpectedly.

Mitigation: Grant only needed permissions and review proposed rules and previews before activation; use rollback when needed.

Risk: Pipeline previews may contact configured webhook or model services.

Mitigation: Use nonsensitive sample requests for previews that contact webhook or model services.

## Reference(s):

- [withHuman MCP server setup](https://withhuman.ai/docs/web-app/mcp-server.md)
- [withHuman approval pipelines](https://withhuman.ai/docs/web-app/approval-pipelines.md)
- [withHuman escalation paths](https://withhuman.ai/docs/web-app/escalation-paths.md)

## Skill Output:

**Output Type(s):** [Configuration, Guidance, API Calls]

**Output Format:** [withHuman pipeline and escalation configuration managed through MCP tools, with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Changes are saved as revisions and can be previewed or rolled back.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
