## Description:

Guides an agent through setting up an EVM wallet, creating a crypto-funded virtual Visa or Mastercard prepaid card through the x402 protocol, and checking card status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyongm](https://clawhub.ai/user/yuanyongm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a dedicated EVM wallet, purchase virtual Visa or Mastercard debit cards with USDT on BSC, and query card order status. The skill is intended for agent-assisted card purchase workflows that require explicit user confirmation before payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw wallet private keys may be exposed through agent context, shell history, process listings, local configuration files, or package behavior.

Mitigation: Use only a dedicated low-balance wallet for card purchases and avoid entering keys from personal or high-value wallets.

Risk: Mutable npx execution can run changed npm package code during financial operations.

Mitigation: Independently verify the package and version before use, and avoid running unpinned npx commands with funds.

Risk: Card creation spends USDT from the configured BSC wallet.

Mitigation: Require explicit user confirmation of the amount before running the create command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanyongm/skills/x402-card)
- [Create Virtual Card](references/create-card.md)
- [Check Card Status](references/check-status.md)
- [Wallet Setup](references/wallet-setup.md)
- [x402 Protocol](references/x402-protocol.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npx, and an EVM_PRIVATE_KEY for wallet-backed card operations.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version is 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
