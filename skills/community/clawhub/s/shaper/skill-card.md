## Description: <br>
Connects an agent to a Shaper workspace through MCP so it can read Shape Up project context, manage scopes, update hill chart progress, and complete work items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jax-agent](https://clawhub.ai/user/jax-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill when they want an agent to work inside a Shaper workspace, orient on active Shape Up cycle work, read pitch specs before implementation, and update scope progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update Shaper project data in a connected workspace. <br>
Mitigation: Install only for workspaces where agent access is intended, use a revocable Shaper API key, and revoke or rotate the key when access is no longer needed. <br>
Risk: API keys may be exposed if pasted into shared chats or logs. <br>
Mitigation: Store the Shaper API key in environment variables or another secret store, and avoid pasting it into shared conversations. <br>
Risk: The referenced agent_register tool can create a provisional Shaper workspace and issue a credential without an existing API key. <br>
Mitigation: Tell the agent not to use agent_register unless the user explicitly wants a new provisional Shaper workspace and credential. <br>


## Reference(s): <br>
- [Shaper MCP Tool Reference](references/tools.md) <br>
- [Shaper MCP Discovery](https://useshaper.com/.well-known/mcp.json) <br>
- [Shaper MCP Endpoint](https://useshaper.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with bash and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Shaper API key and workspace slug for normal authenticated workspace access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
