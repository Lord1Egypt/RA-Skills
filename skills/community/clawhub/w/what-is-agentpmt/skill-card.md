## Description: <br>
This skill explains AgentPMT as an agent management iPaaS platform for connecting agents to platforms, tools, workflows, skills, other agents, payments, OpenClaw agents, and REST API integrations before choosing a setup path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, agents, and developers use this skill to understand AgentPMT's connection model and choose the right account, MCP, REST, AgentAddress, x402, or product-skill setup path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Following linked setup paths can involve bearer tokens, connected accounts, sensitive credentials, payments, or wallets. <br>
Mitigation: Review the separate setup skills before use, protect bearer tokens, and use least-privilege Agent Groups. <br>
Risk: Wallet-funded or payment-enabled workflows can spend funds or act on connected accounts. <br>
Mitigation: Use cautious wallet funding, require appropriate approvals, and validate workflows before allowing production account access. <br>


## Reference(s): <br>
- [AgentPMT Homepage](https://www.agentpmt.com) <br>
- [AgentPMT Marketplace](https://www.agentpmt.com/marketplace) <br>
- [AgentAddress](https://www.agentpmt.com/agentaddress) <br>
- [AgentPMT MCP Server](https://api.agentpmt.com/mcp/) <br>
- [AgentPMT REST Tool Invocation](https://api.agentpmt.com/products/purchase) <br>
- [AgentPMT External API Base](https://www.agentpmt.com/api/external) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with setup-path references and inline URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; directs users to separate setup skills for MCP, REST, AgentAddress, wallet, and x402 workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
