## Description:

Connects an agent to Teambition MCP services to query and manage projects, tasks, members, workflows, comments, files, and related project-management data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeandoom](https://clawhub.ai/user/jeandoom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to connect an agent to a configured Teambition MCP server for project, task, member, workflow, comment, file, and organization operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access credentials through .teambition-token.

Mitigation: Use least-privilege, short-lived tokens; keep .teambition-token out of source control and backups; and restrict local file permissions.

Risk: The skill can perform live project-management changes such as deleting, archiving, modifying members or permissions, and creating upload credentials.

Mitigation: Require explicit user confirmation before destructive or permission-changing actions in a real Teambition workspace.

Risk: The security verdict is suspicious due to broad activation and limited safety guidance.

Mitigation: Review the skill before installation and deployment, especially when connecting it to production Teambition data.

## Reference(s):

- [Teambition MCP configuration page](https://open.teambition.com/user-mcp)
- [Teambition Open Platform documentation](https://open.teambition.com/docs/documents/639982966b99d5002b510f0b)
- [ClawHub skill page](https://clawhub.ai/jeandoom/skills/tb)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with tool names, configuration snippets, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or write local Teambition configuration files and call Teambition MCP tools when configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
