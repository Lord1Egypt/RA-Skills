## Description:

Guides agents through Solana compressed-token distribution using TypeScript examples for simple airdrops, batched airdrops, and custom claim flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tilo-14](https://clawhub.ai/user/tilo-14)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and generate TypeScript patterns for distributing compressed Solana tokens to small or large recipient sets. It also points agents to claim-based distribution references for vesting, clawback, and user-initiated claim workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can sign and submit Solana mainnet transactions with a payer keypair.

Mitigation: Test on devnet or localnet first, keep payer keys in a secrets manager, confirm recipients and total amounts, and simulate or enable preflight before batch execution.

Risk: RPC API keys and payer keys may be exposed if copied directly into scripts.

Mitigation: Load HELIUS_API_KEY and keypairs from managed secrets; do not hard-code them or commit them.

Risk: Token amount arithmetic can be wrong when JavaScript numbers are used for token quantities.

Mitigation: Use bigint or BN-style token amounts and verify mint decimals before sending.

Risk: Large batched distributions can send unintended totals when recipient data or retry settings are wrong.

Mitigation: Deduplicate and review recipient lists, cap batch sizes, log transaction signatures, and reconcile balances after distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tilo-14/skills/solana-token-distribution)
- [ZK Compression documentation](https://www.zkcompression.com)
- [ZK Compression airdrop guide](https://www.zkcompression.com/compressed-tokens/airdrop)
- [Simple Airdrop](references/simple-airdrop.md)
- [Batched Airdrop](references/batched-airdrop.md)
- [@lightprotocol/stateless.js API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html)
- [@lightprotocol/compressed-token API docs](https://lightprotocol.github.io/light-protocol/compressed-token/index.html)
- [Light Protocol audit reports](https://github.com/Lightprotocol/light-protocol/tree/main/audits)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript code blocks and inline configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node for example execution and HELIUS_API_KEY for Helius RPC-backed examples; production use also requires a payer keypair.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
