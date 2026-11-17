## Description:

Build payment flows for Pump Tokenized Agents using @pump-fun/agent-payments-sdk. Use when accepting payments, building accept-payment transactions, integrating Solana wallets, or verifying that a user has paid an invoice on-chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sushant-baton](https://clawhub.ai/user/sushant-baton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Solana payment acceptance, wallet signing flows, and server-side invoice verification to Pump Tokenized Agent applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary says the skill tells agents to follow changeable remote instructions in a payment flow.

Mitigation: Review the skill before production use, prefer bundled reference files or commit-pinned links, and validate payment behavior against trusted project requirements.

Risk: Payment transaction parameters or displayed signing details can diverge from the intended amount, currency, or recipient.

Mitigation: Verify every transaction shown to the user matches the intended amount, currency, and recipient before signing, and confirm payment server-side before delivering the service.

Risk: Unpinned or incompatible npm dependencies can change payment behavior or cause runtime failures.

Mitigation: Pin npm dependencies with a lockfile and align Solana package versions with the @pump-fun/agent-payments-sdk dependency ranges.

Risk: Wallet auto-reconnect can surprise users in a payment flow.

Mitigation: Disclose wallet auto-reconnect behavior and require explicit user confirmation before submitting payment transactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sushant-baton/skills/pump-fun-tokenized-agents)
- [Wallet Integration](references/WALLET_INTEGRATION.md)
- [Scenario Tests](references/SCENARIOS.md)
- [Wallet Integration source reference](https://raw.githubusercontent.com/pump-fun/pump-fun-skills/refs/heads/main/tokenized-agents/references/WALLET_INTEGRATION.md)
- [Scenario Tests source reference](https://raw.githubusercontent.com/pump-fun/pump-fun-skills/refs/heads/main/tokenized-agents/references/SCENARIOS.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, TSX, shell, and environment configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing implementation guidance; it does not sign transactions or handle private keys.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
