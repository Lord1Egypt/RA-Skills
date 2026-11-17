## Description:

Private agent-to-agent payments on Solana using zero-knowledge proofs. Deposit, withdraw, list pools, and estimate fees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentzeny](https://clawhub.ai/user/agentzeny)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to make private Solana payments through SNAP by listing pools, depositing into a shielded pool, withdrawing to a recipient address, estimating withdrawal fees, and checking shielded balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deposits and withdrawals can move funds based on broad natural-language commands.

Mitigation: Require a transaction preview and explicit user confirmation before any deposit or withdrawal is submitted.

Risk: Dependency installation is not pinned to an exact package version.

Mitigation: Pin snap-solana-sdk to a reviewed version and verify the package source before release.

Risk: Viewing keys, notes, RPC endpoints, and relayers can affect payment privacy.

Mitigation: Document how these values are handled and warn users before sharing them with agents, RPC providers, or relayers.

## Reference(s):

- [SNAP public project](https://github.com/agentzeny/snap-public)
- [snap-solana-sdk package](https://www.npmjs.com/package/snap-solana-sdk)
- [Agentzeny website](https://agentzeny.ai)

## Skill Output:

**Output Type(s):** [text, JSON, configuration guidance]

**Output Format:** [Plain text status messages, fee estimates, transaction signatures, and JSON pool listings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SNAP_POOL_ADDRESS and SNAP_RPC_URL; SNAP_RELAYER_URL is optional.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
