## Description:

Operate the local Vibe Kanban instance through the `vibe_kanban` MCP server using `mcporter` to list organizations, projects, issues, and workspaces; create or update issues; start or link workspace sessions; and troubleshoot local dashboard ports on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devbd1](https://clawhub.ai/user/devbd1)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate a local Vibe Kanban MCP server from an agent session, including listing project data, managing issues, starting linked workspace sessions, and locating the local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup example uses an unpinned npm package for the MCP server.

Mitigation: Review the upstream package before installing and use a pinned exact version instead of `@latest`.

Risk: The MCP server can create or update Vibe Kanban data and start workspace sessions from the local account.

Mitigation: Use the server only with an account and workspace where those actions are intended, and review proposed issue or workspace changes before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devbd1/skills/vibe-kanban-mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON arguments for mcporter MCP calls.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
