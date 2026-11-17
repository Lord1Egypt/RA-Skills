## Description:

Manage persistent SSH connections, execute async non-blocking commands, handle concurrent bulk executions across fleets, and manage SSH keys and client assignments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyber-bye](https://clawhub.ai/user/cyber-bye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to guide an agent through SSH connection management, persistent sessions, remote command execution, fleet-wide bulk operations, and key linking through an SSH MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote SSH and fleet-wide command execution can make high-impact changes across target systems.

Mitigation: Require explicit approval for package installs or upgrades, service restarts, file changes, and bulk commands; begin with read-only checks or a single canary host.

Risk: Private keys, connection profiles, sessions, and logs may contain sensitive operational access details.

Mitigation: Verify how the SSH MCP server stores and protects keys, profiles, sessions, and logs before using the skill with production systems.

Risk: Persistent sessions can leave remote resources open if work is not finalized.

Mitigation: Track active sessions and close them at the end of each workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyber-bye/skills/ssh-mcp-cyber-bye)
- [ClawHub publisher profile](https://clawhub.ai/user/cyber-bye)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON MCP tool-call examples and shell command strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and a registered ssh_mcp MCP server with the SSH tools listed in release metadata.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
