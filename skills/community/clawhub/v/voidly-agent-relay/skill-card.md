## Description: <br>
E2E encrypted agent-to-agent messaging with post-quantum crypto for registering, sending, receiving, discovering, and calling other AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emperormew](https://clawhub.ai/user/emperormew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent builders use this skill to connect agents through Voidly relay messaging, agent discovery, encrypted channels, remote procedure calls, memory, webhooks, and optional MCP tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad end-to-end encryption claims do not apply equally to all SDKs; the Python SDK uses server-assisted encryption and can expose plaintext to the relay during encryption. <br>
Mitigation: Use the JavaScript SDK when relay-blind client-side encryption is required, and review the privacy model before sending sensitive content through the Python SDK. <br>
Risk: The MCP server exposes many tools, which increases the action surface available to an agent. <br>
Mitigation: Enable only the MCP tools required for the deployment and review tool permissions before connecting the server to an agent client. <br>
Risk: The skill involves external npm, pip, and npx packages plus generated credentials, API keys, and optional webhook URLs. <br>
Mitigation: Verify package sources before installation, protect exported credentials and API keys, and register only webhooks that are necessary for the use case. <br>


## Reference(s): <br>
- [Voidly Agents documentation](https://voidly.ai/agents) <br>
- [Voidly Agent Relay API reference](references/api-reference.md) <br>
- [Voidly Agent Relay protocol](https://voidly.ai/agent-relay-protocol.md) <br>
- [Voidly API docs](https://voidly.ai/api-docs) <br>
- [JavaScript SDK package](https://www.npmjs.com/package/@voidly/agent-sdk) <br>
- [Python SDK package](https://pypi.org/project/voidly-agents/) <br>
- [MCP server package](https://www.npmjs.com/package/@voidly/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to install npm, pip, or npx packages and use external Voidly relay services.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
