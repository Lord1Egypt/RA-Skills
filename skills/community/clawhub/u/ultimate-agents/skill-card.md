## Description:

AI-powered DeFi agent for automated blockchain transactions, multi-wallet operation, DEX swaps, and adaptive state tracking for dApp interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariesbalweell](https://clawhub.ai/user/ariesbalweell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external DeFi users can use this skill to run an automated blockchain agent that rotates wallets and RPC endpoints, checks market APIs, sends transactions, and attempts DEX swaps. It is most appropriate for controlled testnet or low-value wallet workflows unless stronger transaction approvals and slippage controls are added.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use private keys to execute repeated live blockchain transactions and DEX swaps.

Mitigation: Use testnet or low-value wallets first, keep private keys out of logs, and require per-transaction approval before live use.

Risk: DEX swaps may execute with weak safety controls, including zero minimum output and externally supplied router and token addresses.

Mitigation: Validate RPC, router, and token addresses; add dry-run checks; and require nonzero slippage protection before enabling live swaps.

Risk: Automation depends on runtime configuration and network services that can change or fail.

Mitigation: Pin and update dependencies, monitor failed transactions and API calls, and set conservative transaction-rate limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ariesbalweell/skills/ultimate-agents)
- [Publisher profile](https://clawhub.ai/user/ariesbalweell)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and JSON configuration artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires environment configuration for RPC URLs, private keys, router and token addresses, transaction limits, and delay ranges.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
