## Description:

XferOps Forge helps agents install the Forge MCP server and manage Forge project tasks, boards, columns, comments, and team membership through documented MCP workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parker-xferops](https://clawhub.ai/user/parker-xferops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to configure Forge MCP access, move tickets through the development workflow, add status comments, link pull requests, and administer Forge boards when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow runs @xferops/forge-mcp through npx without a pinned package version.

Mitigation: Pin @xferops/forge-mcp to a reviewed version before installation.

Risk: Forge access depends on FORGE_TOKEN credentials.

Mitigation: Use a least-privilege Forge token and rotate it if setup or usage exposes it.

Risk: Board administration actions can delete projects or columns and add team members.

Mitigation: Restrict board-admin use to authorized operators and review destructive actions before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parker-xferops/skills/xferops-forge)
- [Forge API Service](https://forge.xferops.dev)
- [Forge Skills Overview](artifact/SKILL.md)
- [Forge Setup](artifact/forge-setup/SKILL.md)
- [Forge Dev Workflow](artifact/forge-dev-workflow/SKILL.md)
- [Forge Board Administration](artifact/forge-board-admin/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and Forge MCP tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and proposed MCP actions; execution requires a configured Forge endpoint and token.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
