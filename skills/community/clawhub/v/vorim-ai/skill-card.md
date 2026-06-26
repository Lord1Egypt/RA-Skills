## Description: <br>
Vorim AI provides agent identity, permission checks, trust scores, and audit trails for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kzino](https://clawhub.ai/user/kzino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to register an OpenClaw agent with Vorim, check permissions before sensitive actions, emit audit events after actions, and verify identity or trust when interacting with external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends agent activity metadata to an external Vorim service and maintains a persistent agent identity. <br>
Mitigation: Tell users when activity is being logged, avoid placing private file names or sensitive content in audit event fields, and install only when the user trusts Vorim and the @vorim/mcp-server package. <br>
Risk: The skill requires a Vorim API key and includes credential delegation and token-request capabilities. <br>
Mitigation: Use scoped API keys where possible, keep keys out of source control and logs, and require explicit user approval before delegating credentials or requesting tokens. <br>
Risk: The skill can check or grant permissions for external, financial, or otherwise sensitive actions. <br>
Mitigation: Require explicit user approval before granting permissions or performing financial, external, or privilege-changing actions. <br>


## Reference(s): <br>
- [Vorim AI](https://vorim.ai) <br>
- [Vorim documentation](https://vorim.ai/docs) <br>
- [@vorim/mcp-server npm package](https://www.npmjs.com/package/@vorim/mcp-server) <br>
- [Vorim OpenClaw Skill repository](https://github.com/Kzino/vorim-openclaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with MCP tool calls and shell or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VORIM_API_KEY and the Vorim MCP server.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
