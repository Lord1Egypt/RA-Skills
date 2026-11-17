## Description:

WalletPilot 7715 helps agents execute on-chain transactions with user-granted MetaMask ERC-7715 permissions without sharing private keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreolf](https://clawhub.ai/user/andreolf)

### License/Terms of Use:


## Use Case:

Developers and external agent builders use WalletPilot 7715 to add permissioned wallet connection, token transfers, swaps, balance checks, and transaction history workflows to agents while keeping custody in the user's MetaMask wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated on-chain transactions, swaps, and token transfers can cause irreversible asset loss if permissions, transaction data, or recipients are wrong.

Mitigation: Use a test wallet first, keep permissions short-lived, set low spend limits, restrict allowed chains and contracts, simulate transactions, and require explicit approval before swaps or transfers.

Risk: SDK or API-key misuse could broaden the impact of a compromised agent workflow.

Mitigation: Pin and audit the SDK version, keep API keys narrowly scoped, and review active wallet permissions before deployment.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/andreolf/skills/walletpilot-7715)
- [WalletPilot Documentation](https://docs.walletpilot.xyz)
- [WalletPilot GitHub Repository](https://github.com/andreolf/walletpilot)
- [WalletPilot API Reference](https://api.walletpilot.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API requests and transaction parameter examples for EVM chains.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
