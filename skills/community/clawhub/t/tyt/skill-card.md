## Description:

Connects agents to the Teneo Protocol SDK for wallet-based authentication, room and agent management, messaging, and x402 USDC micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunterdrop22](https://clawhub.ai/user/hunterdrop22)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to integrate with the Teneo Protocol SDK, connect through an Ethereum wallet, discover and invite agents, send room-scoped messages, and handle paid agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys may be exposed or over-privileged if used directly in examples or local environments.

Mitigation: Use a dedicated low-value wallet, keep only minimal USDC for testing, and store the private key only in a secrets manager or tightly controlled environment variable.

Risk: Paid agent calls can spend funds through x402 micropayments.

Mitigation: Treat every paid agent call as capable of spending funds, review token allowances, set practical budgets, and monitor cumulative USDC spend.

Risk: The third-party SDK and payment flow may change or introduce supply-chain risk.

Mitigation: Pin and review the SDK version before installation, and re-review the skill before deploying updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hunterdrop22/skills/tyt)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SDK setup, connection, room management, agent messaging, payment handling, and operational tips.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
