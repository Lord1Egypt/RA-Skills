## Description:

Swap any Solana token from chat by preparing Jupiter quotes, signing with a configured Solana keypair, submitting transactions, checking status, and reporting receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[in-liberty420](https://clawhub.ai/user/in-liberty420)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to quote, confirm, execute, and inspect Solana mainnet token swaps from an agent chat workflow. It is intended for swaps involving SOL and SPL tokens where the user supplies or confirms token mints and controls the configured keypair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign and broadcast real Solana transactions from the configured keypair.

Mitigation: Use only a dedicated low-balance wallet and require manual confirmation of each prepared swap summary before execution.

Risk: The signing flow trusts Jupiter/RPC responses and local prepared swap files at the point of signing.

Mitigation: Review before installing and prefer a version that validates decoded transactions before signing.

Risk: Third-party destinations can move swapped assets outside the keypair owner's wallet.

Mitigation: Avoid third-party destinations unless intended and explicitly confirm the destination address before execution.

Risk: Dependency advisories may remain in the release.

Mitigation: Review and update dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/in-liberty420/skills/solana-easy-swap)
- [Publisher profile](https://clawhub.ai/user/in-liberty420)
- [Jupiter Swap API endpoint](https://lite-api.jup.ag/swap/v1)
- [Default Solana mainnet RPC endpoint](https://api.mainnet-beta.solana.com)
- [Solscan transaction receipt URL pattern](https://solscan.io/tx/{signature})

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI commands return JSON objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and SOLANA_KEYPAIR_PATH; outputs include prepare summaries, transaction signatures, status states, receipts, and structured errors.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
