## Description: <br>
Enables agents to create paid human-executed work and social engagement jobs through EarnFi's x402 Solana USDC API, then poll results with per-job secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earnfidotfun](https://clawhub.ai/user/earnfidotfun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to fund human work such as feedback, labeling, reviews, social engagement, contests, and one-question answer collection. It is intended for workflows where an agent creates paid jobs, saves returned credentials, and later retrieves verifiable submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent coordinate paid human tasks and spend wallet-approved USDC. <br>
Mitigation: Require explicit human confirmation for each spend and use wallet controls that limit available funds. <br>
Risk: Social engagement tasks can create fake popularity, spam, undisclosed promotion, or platform-rule violations. <br>
Mitigation: Review each requested campaign for platform compliance, disclosure requirements, and acceptable-use policy before execution. <br>
Risk: Private keys, agent_token values, and per-job secrets are sensitive bearer credentials. <br>
Mitigation: Keep credentials out of chat, logs, URLs, and shared plaintext files; store them only in an approved secrets manager or local secure storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earnfidotfun/x402-earnfi) <br>
- [Publisher profile](https://clawhub.ai/user/earnfidotfun) <br>
- [EarnFi website](https://earnfi.fun) <br>
- [Agent API base](https://app.earnfi.fun/api/ai-agent/v1) <br>
- [Skill document](https://app.earnfi.fun/skill.md) <br>
- [OpenAPI x402 specification](https://app.earnfi.fun/openapi-x402.json) <br>
- [x402 discovery](https://app.earnfi.fun/.well-known/x402) <br>
- [MCP endpoint](https://app.earnfi.fun/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript examples, endpoint references, and payment-flow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for x402 quote, Solana USDC payment, job creation, polling, and credential handling.] <br>

## Skill Version(s): <br>
1.10.0 (source: server release metadata; artifact frontmatter and package.json report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
