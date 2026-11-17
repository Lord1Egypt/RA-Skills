## Description:

Zyfai Yield Automation helps agents use the Zyfai SDK to connect wallets, deposit supported assets into non-custodial Safe subaccounts, manage automated DeFi yield strategies, and withdraw funds on Ethereum Mainnet, Base, and Arbitrum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldefi](https://clawhub.ai/user/pauldefi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and wallet-enabled agents use this skill to integrate Zyfai SDK flows for DeFi yield deposits, withdrawals, portfolio inspection, strategy updates, and agent registration across supported Ethereum networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to initiate real blockchain deposits, withdrawals, strategy changes, cross-chain settings, and on-chain registration.

Mitigation: Require explicit user approval before every funds-moving transaction, strategy update, cross-chain enablement, or registry action.

Risk: Wallet-enabled use can expose private keys, API keys, and session credentials if raw secrets are used directly.

Mitigation: Pin and lock dependencies, store API keys securely, avoid raw private keys, and prefer wallet providers, WalletClient integrations, KMS, or wallet-as-a-service signers with policy controls.

Risk: Deposited funds are exposed to smart contract, market, protocol, and strategy risk.

Mitigation: Make users confirm supported chains, assets, minimum balances, transaction amounts, and DeFi risk before deposit or withdrawal execution.

## Reference(s):

- [Zyfai SDK documentation](https://docs.zyf.ai)
- [Zyfai API key portal](https://sma.zyf.ai)
- [Programmatic API key creation endpoint](https://sma.zyf.ai/api/sdk-api-keys/create)
- [Zyfai SDK demo](https://github.com/ondefy/zyfai-sdk-demo)
- [Zyfai MCP server](https://mcp.zyf.ai/mcp)
- [Zyfai agent registration metadata](https://www.zyf.ai/.well-known/agent-registration.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can include wallet connection, API key setup, supported-chain constraints, SDK method calls, and transaction approval checkpoints.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
