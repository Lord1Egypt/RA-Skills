## Description:

Provides filesystem operations through MCP stdio, including directory listing, file read and write, directory creation, deletion, and move or rename actions executed by an external go-fs-mcp-server binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgwventrue](https://clawhub.ai/user/lgwventrue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to request filesystem tasks from an agent using natural language or structured tool parameters. It is intended for environments where the operator has configured the external MCP server and is comfortable granting it filesystem authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad file read, write, delete, and move authority through external binaries without clear path limits or verified runtime pinning.

Mitigation: Install only after verifying the upstream source and dependencies, configure the narrowest possible filesystem scope, and avoid running OpenClaw with elevated privileges.

Risk: Delete, move, and overwrite requests can cause data loss if issued incorrectly or through an unsafe agent workflow.

Mitigation: Review high-impact filesystem requests before execution and use cautious operating-system permissions or backups for sensitive paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lgwventrue/skills/system-file-handler)
- [go-fs-mcp Repository](https://github.com/go-fs-mcp/go-fs-mcp)
- [go-fs-mcp Operations Documentation](https://github.com/go-fs-mcp/go-fs-mcp/blob/main/docs/OPERATIONS.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and filesystem operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured go-fs-mcp-skill and go-fs-mcp-server binaries; filesystem effects depend on the requested operation and server permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
