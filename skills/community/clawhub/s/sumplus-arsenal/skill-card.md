## Description:

Execute DeFi skills on Ethereum, Sui, Solana, and 10+ chains via Arsenal for swaps, lending, liquidity, portfolio queries, and blockchain operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sumplus-real](https://clawhub.ai/user/sumplus-real)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to route DeFi requests through Arsenal's discovery and execution API across supported EVM, Sui, Solana, and cross-chain protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote-generated DeFi transaction payloads can cause irreversible asset transfers, approvals, or other high-impact blockchain actions.

Mitigation: Require the user to inspect wallet transaction details, including recipients, approvals, token amounts, chain, contract addresses, and persistent allowances before signing.

Risk: Quotes or skill descriptions may not fully validate the final transaction payload.

Mitigation: Do not treat quotes as authorization to sign; obtain explicit confirmation after presenting quote details and before building or submitting a transaction.

Risk: API key creation and use creates an account-management dependency on Arsenal/Sumplus.

Mitigation: Treat API key creation as an explicit user-approved account action and require ARSENAL_API_KEY to be supplied through the environment.

## Reference(s):

- [Arsenal homepage](https://arsenal.sumplus.xyz)
- [ClawHub skill page](https://clawhub.ai/sumplus-real/skills/sumplus-arsenal)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARSENAL_API_KEY and user review before wallet signing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
