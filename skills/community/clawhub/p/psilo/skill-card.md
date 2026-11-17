## Description:

Use this skill when an agent needs to create on-chain escrow contracts via EscrowFactory, release escrowed funds via arbiter-signed transactions, and interact with the Pakt Escrow service using the @pakt/psilo SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pakt](https://clawhub.ai/user/pakt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create, fund, monitor, and release EVM escrow contracts through the Pakt Psilo SDK and escrow API. It is intended for workflows that require explicit wallet authentication, signed transaction payloads, and buyer/seller release confirmations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe ERC-20 deposit guidance could cause token loss if an agent signs the example transaction as written.

Mitigation: Confirm the escrow contract deposit flow against authoritative contract documentation, prefer SDK-provided approve and deposit payloads, and decode every transaction before signing.

Risk: Escrow create, deposit, update, and release workflows can move or release real funds.

Mitigation: Require explicit user confirmation, enforce chain and token allowlists, apply spend limits, and test on testnets or with small limits before production use.

Risk: Wallet, bearer token, and release-secret handling can expose sensitive credentials.

Mitigation: Redact tokens and secrets from logs, never store private keys or release secrets in repository files, and pin and audit wallet and signing dependencies before use.

## Reference(s):

- [@pakt/psilo SDK](https://www.npmjs.com/package/@pakt/psilo)
- [SIWA skill documentation](https://siwa.id/skill.md)
- [SIWA protocol specification](https://siwa.id/docs)
- [Evalanche package](https://www.npmjs.com/package/evalanche)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, API calls]

**Output Format:** [Markdown with TypeScript, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces escrow workflow instructions, SDK call patterns, authentication guidance, and transaction preparation examples.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
