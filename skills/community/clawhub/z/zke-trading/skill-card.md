## Description:

ZKE AI Master Trader (Official). Control spot and futures trading, manage assets, and access real-time market data on ZKE Exchange.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zke-exchange](https://clawhub.ai/user/zke-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and developers use this skill to access ZKE Exchange market data, account balances, spot and margin orders, futures positions, transfers, and withdrawals through an OpenClaw/MCP tool interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real trades, move funds between accounts, change futures settings, cancel orders, and request withdrawals.

Mitigation: Use API keys with withdrawals disabled, minimal trading permissions, IP allowlisting, and account-level limits; require explicit user confirmation before any trade or fund movement.

Risk: Sensitive trading activity, balances, parameters, or withdrawal addresses may be written to the local OpenClaw plugin log.

Mitigation: Review or disable the local log at ~/.zke-trading/openclaw-plugin.log before using the skill with sensitive balances or withdrawal addresses.

Risk: The security evidence reports weak enforced safeguards for high-impact trading and withdrawal operations.

Mitigation: Install only in a trusted host environment where operators understand the live-account impact and can enforce account-level limits and approval workflows.

## Reference(s):

- [ZKE Skill Guide](https://support.zke.com/skills/)
- [ZKE Website](https://zke.com)
- [ZKE Trading SDK GitHub Repository](https://github.com/ZKE-Exchange/zke-trading-sdk)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON tool responses and concise Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZKE_API_KEY and ZKE_SECRET_KEY; actions can affect live ZKE Exchange accounts.]

## Skill Version(s):

1.0.13 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
