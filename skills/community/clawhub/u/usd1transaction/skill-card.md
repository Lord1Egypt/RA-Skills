## Description:

Securely transfer USD1 (USDC on Wormhole) between wallets using Wormhole Liquidity Facility on testnet by default.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[asgherali](https://clawhub.ai/user/asgherali)

### License/Terms of Use:

ISC

## Use Case:

Developers and agents use this skill to execute USD1 testnet transfers between wallets and return the transaction hash, status, and message. It is suitable for controlled testnet workflows that require explicit handling of amount, recipient address, source chain, and a sender key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a raw wallet private key and can broadcast token transfers.

Mitigation: Use only disposable testnet wallets, never provide keys that control real funds or are reused on mainnet, and require explicit human confirmation before sending.

Risk: Transfer confirmation and input validation are not strong enough for real-value transfers.

Mitigation: Add strict amount, address, and chain validation, keep dependencies updated, and prefer wallet or signer integration before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asgherali/skills/usd1transaction)

## Skill Output:

**Output Type(s):** [JSON, text]

**Output Format:** [JSON object with transactionHash, status, and message fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May broadcast a Wormhole testnet transfer when valid inputs and a sender key are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
