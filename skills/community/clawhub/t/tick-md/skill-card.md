## Description:

Coordinate work across human and AI agents through Git-backed TICK.md task files, with CLI and MCP workflows for task status, claiming, comments, dependency tracking, and synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gianni-dalerta](https://clawhub.ai/user/gianni-dalerta)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use tick-md to coordinate project work across humans and AI agents by creating, claiming, updating, and reviewing tasks in TICK.md through shell commands or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change local task files while coordinating work.

Mitigation: Review task changes before relying on them, keep the MCP server scoped to the intended project, and confirm before delete, force-delete, direct status edits, or undo operations.

Risk: The skill relies on globally installed npm tools and editor MCP configuration.

Mitigation: Prefer pinned or locally reviewed versions of tick-md and tick-mcp-server, back up config files, and approve MCP config edits deliberately.

Risk: Git synchronization can send project task data to a remote.

Mitigation: Use pull-only sync by default and run tick sync --push or git push only after explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gianni-dalerta/skills/tick-md)
- [GitHub repository](https://github.com/Purple-Horizons/tick-md)
- [Installation guide](artifact/INSTALL.md)
- [MCP tools reference](artifact/mcp-reference.md)
- [tick-md npm package](https://npmjs.com/package/tick-md)
- [tick-mcp-server npm package](https://npmjs.com/package/tick-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with shell commands, JSON configuration, and MCP tool examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local TICK.md edits, MCP configuration changes, and git synchronization commands; remote pushes require explicit user approval.]

## Skill Version(s):

1.3.3 (source: evidence release, skill.json, CHANGELOG released 2026-02-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
