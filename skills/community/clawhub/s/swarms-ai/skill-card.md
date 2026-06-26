## Description: <br>
Build and orchestrate multi-agent AI systems using the Swarms API, including single agents, swarms, streaming responses, sub-agent delegation, marketplace publishing, ATP payments, and Solana token launches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NewSoulOnTheBlock](https://clawhub.ai/user/NewSoulOnTheBlock) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement Swarms API workflows for single-agent, reasoning-agent, and multi-agent orchestration. It provides practical guidance for API configuration, agent architecture selection, streaming, tool integration, marketplace publishing, and paid blockchain-related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid blockchain workflows may send raw Solana wallet private keys to remote services. <br>
Mitigation: Use a dedicated low-balance or test wallet, never a main wallet, and require explicit approval before token launches or ATP payments. <br>
Risk: API keys, wallet keys, or MCP credentials could be exposed through prompts, logs, or over-broad tool access. <br>
Mitigation: Keep secrets in environment variables, avoid including secrets in prompts or logs, restrict autonomous tools with selected_tools, and connect only trusted MCP servers with least-privilege tokens. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/NewSoulOnTheBlock/swarms-ai) <br>
- [Swarms docs index](https://docs.swarms.ai/llms.txt) <br>
- [Swarms API keys](https://swarms.world/platform/api-keys) <br>
- [Swarms marketplace](https://swarms.world) <br>
- [Swarms API Architecture](references/architecture.md) <br>
- [Sub-Agent Delegation](references/sub-agents.md) <br>
- [ATP Agent Trade Protocol](references/atp-protocol.md) <br>
- [Swarms Marketplace](references/marketplace.md) <br>
- [Streaming Responses](references/streaming.md) <br>
- [Tools Integration](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Python, JSON, endpoint, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request patterns, agent configuration tables, architecture choices, streaming handling, tool configuration, and wallet-safety guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
