## Description:

x402 payment layer for AI agents that charges USDC per skill call and wraps skills with per-call pricing and on-chain payment verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strouddustinn-bot](https://clawhub.ai/user/strouddustinn-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to add x402-style USDC payment requirements to agent skill calls, verify payments, and track payment activity in a ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Core payment verification and automatic payment behavior are unsafe for real-money use without careful review.

Mitigation: Do not use for production or autonomous real-money payments until payment verification, spending approval, trusted recipient controls, and replay handling are reviewed and fixed.

Risk: Payment verification may not validate the actual USDC transfer details.

Mitigation: Validate the recipient, sender, amount, token contract, chain, and confirmation status for each transaction, and fail closed when dependencies or RPC checks fail.

Risk: Transaction replay protection may not be durable across process restarts.

Mitigation: Persist used transaction hashes in the ledger before accepting payment and reject reused transaction hashes across service instances.

## Reference(s):

- [Agent Economy Docs](https://agent-economy.io/docs)
- [x402 Spec](https://x402.dev)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes HTTP 402 payment response shapes, payment client behavior, and ledger usage patterns.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
