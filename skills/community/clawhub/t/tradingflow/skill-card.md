## Description:

Create and manage crypto trading strategies, deploy automated trading bots, and control on-chain vaults on BSC, Aptos, and Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thecleopatra](https://clawhub.ai/user/thecleopatra)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and TradingFlow users use this skill to create, deploy, monitor, and manage automated trading strategies, on-chain vault operations, webhooks, and strategy hub workflows through an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage TradingFlow strategies and potentially automate crypto trades.

Mitigation: Install only for intentional TradingFlow trading automation, use a dedicated low-balance vault, start with swap-only permissions, and set conservative spending limits.

Risk: Stored signing keys and autonomous bots can increase execution risk.

Mitigation: Avoid storing private keys unless autonomous execution risk is accepted, keep private-key storage behind the R&D Mode gate, and grant only the minimum permissions needed.

Risk: External triggers and API configuration can route trading actions through unsafe inputs or endpoints.

Mitigation: Require signed webhooks, pin dependencies, and keep TRADINGCLAW_BASE_URL on the official HTTPS API endpoint.

## Reference(s):

- [TradingFlow Homepage](https://tradingflow.fun)
- [TradingFlow API Reference](references/api-reference.md)
- [Strategy Format Reference](references/strategy-format.md)
- [Vault Operations Guide](references/vault-operations.md)
- [Webhooks & Triggers](references/webhook-triggers.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API calls and approval links for user-reviewed blockchain transactions.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
