## Description:

TypeScript SDK guidance for the 8004 Trustless Agent Registry on Solana, covering agent registration, feedback and SEAL v1, ATOM reputation, signing, indexer queries, x402 payment feedback, and skipSend server-mode patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montecrypto999](https://clawhub.ai/user/montecrypto999)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure and use the 8004 Solana TypeScript SDK for on-chain agent registration, reputation feedback, signing, indexer-backed reads, and related registry workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to use a raw wallet private key for write-enabled Solana operations.

Mitigation: Use a low-value delegated wallet, keep private keys out of broad agent environments when possible, and prefer external signing or skipSend flows.

Risk: The skill includes irreversible blockchain writes, including registration, feedback, transfers, metadata deletion, and immutable metadata writes.

Mitigation: Require explicit human confirmation before transfers, metadata deletion, immutable metadata writes, or other on-chain mutations.

Risk: The skill relies on npm packages and indexer or RPC services for some workflows.

Mitigation: Pin and review npm dependencies, use trusted RPC and indexer endpoints, and verify indexer integrity before relying on indexed data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/montecrypto999/skills/solana-agent-registry)
- [8004 Solana TypeScript SDK homepage](https://github.com/QuantuLabs/8004-solana-ts)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only examples can run without a wallet; write-enabled examples require Node.js and a Solana private key environment variable.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata); SDK 0.6.3 (source: artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
