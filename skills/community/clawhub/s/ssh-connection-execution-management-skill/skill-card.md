## Description: <br>
Manage persistent SSH connections, execute async non-blocking commands, handle concurrent bulk executions across fleets, and manage SSH keys and client assignments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyber-bye](https://clawhub.ai/user/cyber-bye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and infrastructure teams use this skill to manage SSH connection lifecycles, run remote commands, monitor asynchronous execution, and coordinate bulk operations across server fleets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can administer remote servers, including fleet-level commands that may cause downtime or broad configuration changes. <br>
Mitigation: Use approved host scopes, least-privilege deploy accounts, and require explicit confirmation before upgrades, restarts, or other disruptive commands. <br>
Risk: The skill handles SSH keys and sensitive remote-access credentials. <br>
Mitigation: Use passphrase-protected keys, restricted file permissions, approved key storage, and avoid placing plaintext private keys in connection files or scripts. <br>
Risk: The security scan summary reports insufficient built-in safeguards for SSH keys and fleet-level disruptive commands. <br>
Mitigation: Install only when the publisher is trusted and review planned remote actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyber-bye/ssh-connection-execution-management-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples and shell command strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ssh_mcp MCP server and the listed SSH MCP tools to be available.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
