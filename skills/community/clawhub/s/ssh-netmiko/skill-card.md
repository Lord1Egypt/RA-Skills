## Description: <br>
Provides agents with MCP tools to create and close SSH sessions, run commands on remote devices, check service health, and inspect active session and command history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[is-the-king](https://clawhub.ai/user/is-the-king) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and network administrators use this skill to manage SSH sessions and run commands on systems they control through the MCP_Server_Trigger server. It supports session creation, command execution, active-session inspection, session and command history review, health checks, and session closure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent run broad SSH commands on remote systems. <br>
Mitigation: Use it only with systems you control, restrict allowed hosts and commands, and require explicit approval before changes are executed. <br>
Risk: The skill handles SSH credentials and can create sessions with username and password inputs. <br>
Mitigation: Use least-privilege credentials, avoid shared administrative accounts, and verify the external MCP server and mcp2skill source before installation. <br>
Risk: Session and command history may expose sensitive operational details. <br>
Mitigation: Confirm how the external service stores, protects, and deletes session and command history before use. <br>


## Reference(s): <br>
- [MCP Tools Reference](references/TOOLS.md) <br>
- [mcp2skill](https://github.com/fenwei-dev/mcp2skill) <br>
- [ClawHub skill page](https://clawhub.ai/is-the-king/ssh-netmiko) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Text or JSON-like MCP tool responses containing command output, session status, health status, or history records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include remote command results and session or command history from the external SSH service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
