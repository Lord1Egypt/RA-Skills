## Description:

Understand AgentPMT as an agent management iPaaS platform for connecting agents to hundreds of platforms, tools, workflows, skills, other agents, payments, OpenClaw agents, and REST API integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to understand AgentPMT capabilities and choose between account-based MCP or REST setup, no-account AgentAddress/x402 access, or product-specific AgentPMT skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AgentPMT bearer tokens can grant access to configured tools, workflows, agents, skills, and credentials.

Mitigation: Keep bearer tokens secret and use the least-privileged Agent Group that supports the task.

Risk: No-account AgentAddress and x402 paths may use credits or payment-capable wallets.

Mitigation: Confirm credit-backed or x402 costs before execution.

Risk: Third-party tools or connected services may receive task data during downstream AgentPMT use.

Mitigation: Avoid sending sensitive data to third-party tools unless the task requires it.

## Reference(s):

- [AgentPMT](https://www.agentpmt.com)
- [AgentPMT Marketplace](https://www.agentpmt.com/marketplace)
- [AgentAddress](https://www.agentpmt.com/agentaddress)
- [AgentPMT MCP Server](https://api.agentpmt.com/mcp/)
- [REST Tool Invocation](https://api.agentpmt.com/products/purchase)
- [External No-Account API Base](https://www.agentpmt.com/api/external)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with links, setup-path recommendations, and inline endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No credentials are required to read the skill; downstream AgentPMT setup paths may require bearer tokens, credits, or x402-capable payment setup.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
