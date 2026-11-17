## Description:

Connects an agent to a local self-custody Ethereum wallet for reading balances and DeFi positions, previewing transactions, and sending funds when the user grants execution access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rustok](https://clawhub.ai/user/rustok)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet owners and developers use this skill to let an agent inspect Ethereum wallet balances and DeFi positions and preview transactions. With explicit permission, the agent can submit transactions for separate human approval or, after the owner enables autonomous mode, without per-transaction approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous mode can send real funds without per-transaction approval or built-in spending limits.

Mitigation: Keep the wallet read-only or supervised unless autonomous spending is intentional, and fund it only with money you can afford to lose.

Risk: Exposing the recovery phrase or approval PIN could compromise the wallet.

Mitigation: Back up the recovery phrase offline and enter the PIN and recovery phrase only in the owner's own terminal, never in agent chat.

Risk: A broadcast transaction may fail on-chain, and retrying an uncertain payment can duplicate it.

Mitigation: Confirm the on-chain receipt before reporting success and resolve pending or unknown payments before retrying.

## Reference(s):

- [Rustok Agentic Wallet on ClawHub](https://clawhub.ai/rustok/skills/wallet)
- [Wallet security caveats](https://github.com/rustok-org/mcp/blob/main/docs/CAVEATS.md)
- [Sigstore installation guidance](https://docs.sigstore.dev/cosign/system_config/installation/)

## Skill Output:

**Output Type(s):** [Text, Transaction previews, Transaction status]

**Output Format:** [Text and structured wallet tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet balances, DeFi positions, transaction risk previews and execution status; a broadcast transaction is not necessarily confirmed on-chain.]

## Skill Version(s):

0.12.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
