## Description:

Monitors token prices across major decentralized exchanges, tracks cross-DEX spreads, configures price alerts, analyzes trends, and suggests trade paths across Ethereum, Arbitrum, BSC, and related DeFi ecosystems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External DeFi users, crypto traders, analysts, and developers use this skill to compare DEX prices, monitor spreads, configure alerts, review historical movement, and evaluate possible trading routes. Outputs should be treated as monitoring and analysis signals rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment integration may charge 0.01 USDT per invocation and sends the SkillPay user ID to skillpay.me.

Mitigation: Install and invoke only after confirming trust in the publisher and SkillPay flow; use explicit consent, budget controls, and minimal exposure of SkillPay user identifiers.

Risk: A hard-coded payment API key is exposed in the artifact and should be considered compromised.

Mitigation: Rotate or revoke the exposed key before release and require payment credentials to be supplied through managed secrets or environment variables.

Risk: DEX prices, spreads, and route suggestions may be delayed, inaccurate, or affected by liquidity, gas, slippage, or API limits.

Mitigation: Treat outputs as monitoring signals, not investment advice; independently verify price, liquidity, gas, and slippage before executing trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-dex-price-monitor)
- [Price Data Sources Guide](artifact/references/data-sources.md)
- [Monitoring Tools Guide](artifact/references/monitoring-tools.md)
- [API Documentation Quick Reference](artifact/references/api-documentation.md)
- [Alert Configuration Guide](artifact/references/alert-configuration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables, code snippets, configuration examples, and optional Python script commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live API calls, webhook notification setup, DEX price comparisons, alert definitions, route quotes, and paid SkillPay billing checks.]

## Skill Version(s):

2025.4.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
