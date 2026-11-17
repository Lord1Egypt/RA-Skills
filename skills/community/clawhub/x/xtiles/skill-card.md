## Description:

Create and manage structured visual pages, projects, tiles, tasks and workflows in xTiles via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtiles](https://clawhub.ai/user/xtiles)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to their own xTiles workspace, read workspace structure, and manage projects, pages, tiles, tasks, layouts, collections, planners, workflows, and user context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can access and change the user's real xTiles workspace after authentication.

Mitigation: Install the skill only when workspace access is intended, operate only on user-requested resources, and review write requests before execution.

Risk: Some supported actions can overwrite content or permanently delete tasks.

Mitigation: Confirm intent before destructive actions, especially irreversible task deletion.

Risk: Legacy personal access tokens are accepted as bearer tokens.

Mitigation: Prefer OAuth login over legacy personal access tokens when possible.

## Reference(s):

- [xTiles ClawHub Skill Page](https://clawhub.ai/xtiles/skills/xtiles)
- [xTiles Homepage](https://xtiles.app)
- [xTiles MCP Endpoint](https://mcp.xtiles.app/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected user's xTiles workspace and hosted MCP tools; exact tool names and JSON schemas are resolved from the MCP endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
