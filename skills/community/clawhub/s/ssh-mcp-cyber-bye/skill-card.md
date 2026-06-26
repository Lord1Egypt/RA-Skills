## Description: <br>
Manage persistent SSH connections, execute async non-blocking commands, handle concurrent bulk executions across fleets, and manage SSH keys and client assignments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyber-bye](https://clawhub.ai/user/cyber-bye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage SSH-accessible Linux servers, reuse persistent sessions, monitor asynchronous command execution, run bulk fleet operations, and manage SSH keys and client assignments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables high-impact SSH administration across single servers and fleets. <br>
Mitigation: Require explicit approval before upgrades, restarts, file changes, key changes, and bulk commands, including target hosts, exact commands, expected impact, and rollback or verification steps. <br>
Risk: Bulk execution can spread an incorrect command across multiple hosts. <br>
Mitigation: Start with a limited target set, review command intent and concurrency, monitor status and logs, and expand only after verifying expected results. <br>
Risk: SSH keys and connection records are sensitive credentials. <br>
Mitigation: Use the key-management flow rather than hardcoding private keys, restrict access to stored keys, and confirm key links before running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyber-bye/ssh-mcp-cyber-bye) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with MCP tool call examples and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a registered ssh_mcp server and node runtime.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
