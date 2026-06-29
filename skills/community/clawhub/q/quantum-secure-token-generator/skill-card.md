## Description: <br>
Guides agents in generating configurable random tokens for API keys, session tokens, password resets, and related authentication workflows through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request configurable tokens for API keys, session identifiers, password resets, 2FA codes, secure URLs, and cryptographic nonces from the AgentPMT-hosted tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be used in contexts that involve account credentials, wallet details, payment headers, or other sensitive setup data. <br>
Mitigation: Keep credentials out of prompts and logs, use the AgentPMT setup workflow for credential handling, and grant only the minimum access needed for the intended tool call. <br>
Risk: Generated tokens are secrets and can authorize access if exposed. <br>
Mitigation: Store generated tokens immediately in an appropriate secret manager or secure destination, and avoid printing or retaining them in chat transcripts, logs, or shared files. <br>
Risk: The skill invokes a remote AgentPMT product that can consume credits and depends on the live service schema. <br>
Mitigation: Confirm the selected tool, action, parameters, and live schema before production use, especially when endpoint behavior or examples may have changed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/quantum-secure-token-generator) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/quantum-secure-token-generator) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [AgentPMT MCP Server](https://api.agentpmt.com/mcp/) <br>
- [AgentPMT REST Invoke Endpoint](https://api.agentpmt.com/products/purchase) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated tokens are returned as strings; token length is configurable from 8 to 256 characters with selectable charset and randomness source.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
