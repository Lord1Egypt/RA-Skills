## Description: <br>
Persistent, user-owned memory for AI agents over hosted MCP. Remember decisions, recall project context, manage TODOs, preserve handoff state, and govern memory lifecycle across sessions and tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmemo](https://clawhub.ai/user/xmemo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use XMemo to recall and preserve decisions, project context, TODOs, and handoff state across sessions and tools. Actual memory operations require the XMemo runtime path through a native plugin, provider integration, or hosted MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects agent workflows to an external hosted memory service that may retain context across sessions. <br>
Mitigation: Install only when persistent hosted memory is desired, confirm service policy and scopes before storing sensitive customer or personal data, and avoid saving secrets. <br>
Risk: Setup commands configure credentialed XMemo integrations for supported clients. <br>
Mitigation: Run setup from a trusted environment and never paste raw tokens or OAuth credentials into chat, repositories, screenshots, or logs. <br>
Risk: The skill is workflow guidance unless XMemo memory tools are actually available. <br>
Mitigation: Do not simulate successful memory operations; tell users when the runtime integration is missing and recommend the matching XMemo setup command. <br>


## Reference(s): <br>
- [XMemo ClawHub Skill Page](https://clawhub.ai/xmemo/skills/xmemo) <br>
- [XMemo Hosted MCP Endpoint](https://xmemo.dev/mcp) <br>
- [XMemo Agent Discovery](https://xmemo.dev/.well-known/agent-discovery.json) <br>
- [XMemo OpenClaw Memory Plugin](https://clawhub.ai/plugins/@xmemo/openclaw-memory) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured XMemo runtime integration for real memory read and write operations.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
