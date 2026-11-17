## Description:

Transfers USD1 (USDC on Wormhole) between wallets using Wormhole Liquidity Facility on testnet and returns a transaction hash, status, and message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asgherali](https://clawhub.ai/user/asgherali)

### License/Terms of Use:

ISC

## Use Case:

Developers and agents use this skill to initiate testnet USD1 transfers after receiving an amount, recipient address, chain, and sender key, then report the resulting transaction status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a raw wallet private key, which can expose funds if the key is reused, stored, or logged.

Mitigation: Use only a disposable testnet wallet key that controls no real funds, and replace raw private-key input with a constrained wallet or signer flow before broader use.

Risk: The skill can send tokens without a final transaction preview or confirmation step.

Mitigation: Add an explicit transaction preview and user confirmation before submitting any transfer.

Risk: Invalid chain, address, or amount inputs could cause failed or unintended transfer attempts.

Mitigation: Validate chain, recipient address, and amount exactly before constructing the transaction.

Risk: Dependency and network behavior may change over time.

Mitigation: Pin and regularly update dependencies, and restrict network access to the required testnet endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asgherali/skills/usd1)
- [Publisher profile](https://clawhub.ai/user/asgherali)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON object with transactionHash, status, and message fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires amount, recipient address, and sender private key as inputs; chain defaults to Solana.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
