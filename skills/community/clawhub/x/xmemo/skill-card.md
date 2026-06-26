## Description: <br>
Persistent, user-owned memory for AI agents over hosted MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmemo](https://clawhub.ai/user/xmemo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use XMemo to let authorized agents recall and maintain durable project context, decisions, TODOs, and handoff state across sessions and tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users or agents may store secrets, tokens, or sensitive personal or customer data in long-term memory. <br>
Mitigation: Use scoped API keys or OAuth and do not store secrets or sensitive data unless there is an explicit need and appropriate privacy controls. <br>
Risk: Authorized agents may recall visible user-owned memories written by other agents, exposing broader context than intended for a task. <br>
Mitigation: Use narrower project, bucket, or scope filters when the user requests limited recall, and treat attribution fields as provenance rather than authorization proof. <br>
Risk: Delete, forget, redact, overwrite, or broad cleanup actions can remove useful memory state. <br>
Mitigation: Confirm the exact target before destructive memory operations. <br>
Risk: Recalled memories can be stale or incomplete compared with current files or external service state. <br>
Mitigation: Treat recalled memories as context and verify drift-prone facts when correctness matters. <br>


## Reference(s): <br>
- [XMemo Skill on ClawHub](https://clawhub.ai/xmemo/skills/xmemo) <br>
- [XMemo OpenClaw Memory Plugin](https://clawhub.ai/plugins/@xmemo/openclaw-memory) <br>
- [XMemo MCP Server](https://xmemo.dev/mcp) <br>
- [XMemo Agent Discovery](https://xmemo.dev/.well-known/agent-discovery.json) <br>
- [XMemo OpenClaw MCP Configuration](https://xmemo.dev/v1/mcp/config/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP setup URLs and tool-use recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actual memory operations require the XMemo MCP server and user authorization.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
