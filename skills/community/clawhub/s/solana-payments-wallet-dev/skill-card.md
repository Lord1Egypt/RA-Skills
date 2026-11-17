## Description:

Guides developers building Solana stablecoin payment flows and wallet integrations with light-token, including receive and send flows, balances, history, client-side signing, and optional nullifiers to prevent duplicate execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilo-14](https://clawhub.ai/user/tilo-14)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and implement Solana stablecoin payments and wallet UX using light-token, wallet adapters, Privy signing, and nullifier patterns for duplicate-action prevention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment, transfer, wrap, and unwrap examples can affect real funds.

Mitigation: Review generated transactions before signing and validate recipient, mint, amount, decimals, cluster, and serialized transaction contents.

Risk: Privy signing flows involve app secrets and treasury authorization keys.

Mitigation: Keep Privy credentials in server-side secret storage only and verify signing requests are sent only to Privy's official endpoints.

Risk: Unpinned skill or npm dependency versions can change behavior between installs.

Mitigation: Pin the skill source and npm dependencies before production use.

Risk: Generating a fresh random nullifier ID during retries can bypass duplicate-action protection.

Mitigation: Use a deterministic or persisted operation identifier for nullifier retries.

## Reference(s):

- [Payments](references/payments.md)
- [Wallets](references/wallets.md)
- [Signing with wallet adapters](references/sign-with-adapter.md)
- [Signing with Privy](references/sign-with-privy.md)
- [Nullifier PDAs](references/nullifiers.md)
- [ZK Compression documentation](https://www.zkcompression.com)
- [Light-token payments documentation](https://zkcompression.com/light-token/toolkits/for-payments)
- [Light-token wallets documentation](https://zkcompression.com/light-token/toolkits/for-wallets)
- [Light Protocol stateless.js API documentation](https://lightprotocol.github.io/light-protocol/stateless.js/index.html)
- [Light Protocol compressed-token API documentation](https://lightprotocol.github.io/light-protocol/compressed-token/index.html)
- [Light Protocol nullifier program package](https://www.npmjs.com/package/@lightprotocol/nullifier-program)
- [Light Protocol examples for payments and wallets](https://github.com/Lightprotocol/examples-light-token/tree/main/toolkits/payments-and-wallets)
- [Light Protocol audit reports](https://github.com/Lightprotocol/light-protocol/tree/main/audits)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript, Rust, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction-building and signing guidance that must be reviewed before use with real funds.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
