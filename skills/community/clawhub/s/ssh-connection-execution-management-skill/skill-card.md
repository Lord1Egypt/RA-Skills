## Description:

Manage persistent SSH connections, execute async non-blocking commands, handle concurrent bulk executions across fleets, and manage SSH keys and client assignments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyber-bye](https://clawhub.ai/user/cyber-bye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to manage SSH connection lifecycles, run remote commands, inspect logs, organize client fleets, and coordinate bulk administrative tasks across Linux servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through powerful SSH actions, including upgrades, restarts, file changes, key imports, and bulk execution across fleets.

Mitigation: Require explicit human approval before those actions and verify the target client, host list, maintenance window, health checks, and rollback plan.

Risk: The skill depends on the referenced ssh_mcp server to manage real SSH targets.

Mitigation: Install and use the skill only when the ssh_mcp server is trusted, registered with the MCP host, and appropriate for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyber-bye/skills/ssh-connection-execution-management-skill)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool-call examples and inline command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance depends on the ssh_mcp MCP server and node binary being available.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
