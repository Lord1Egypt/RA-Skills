## Description:

Provides an AI agent with a local Sui wallet server and Chrome extension for managing accounts, switching networks, signing transactions, and interacting with Sui DApps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:


## Use Case:

Developers building or testing Sui DApps use this skill to give an agent a local wallet interface for account management, test transactions, signing flows, and Wallet Standard integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Seed phrases and wallet administration are exposed through local HTTP APIs.

Mitigation: Use only disposable or unfunded wallets until authentication, origin restrictions, and removal of HTTP mnemonic export are implemented.

Risk: Signing and execution capabilities can affect real Sui assets, especially on mainnet.

Mitigation: Require explicit per-transaction review and approval, and avoid funded mainnet wallets unless the server has been redesigned with stronger controls.

Risk: The browser extension uses a broad page surface for DApp interaction.

Mitigation: Scope extension permissions and allowed origins to trusted DApps before production or funded use.

## Reference(s):

- [Sui Agent Wallet on ClawHub](https://clawhub.ai/easonc13/skills/sui-agent-wallet)
- [Sui Testnet Faucet](https://faucet.testnet.sui.io/)
- [Sui Devnet Faucet](https://faucet.devnet.sui.io/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, curl commands, configuration steps, and local API usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operating guidance for a local Bun server, Chrome extension, Sui wallet APIs, transaction approval flows, and a test DApp.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
