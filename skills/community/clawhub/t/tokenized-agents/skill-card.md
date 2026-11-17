## Description:

Guides agents through Solana payment flows using @pump-fun/agent-payments-sdk to build payment transactions, verify invoice payments, and integrate wallet adapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maliot100x](https://clawhub.ai/user/maliot100x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add user-approved Solana payment flows to agent actions, including invoice parameter collection, transaction construction, wallet signing, and server-side payment verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable external wallet and scenario documentation can change after release.

Mitigation: Review or vendor the referenced documentation before use instead of allowing an agent to follow mutable main-branch URLs unchecked.

Risk: Loosely constrained wallet and payment dependencies can introduce incompatible or unexpected package versions.

Mitigation: Pin dependency versions, use a reviewed lockfile, and align shared Solana package versions with the payment SDK before installation.

Risk: Payment workflows can expose sensitive wallet material or move funds without appropriate user control.

Mitigation: Keep transaction signing user-approved, never provide private keys or seed phrases, and verify payments server-side before delivering paid services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maliot100x/skills/tokenized-agents)
- [Server-Resolved Source Repository](https://github.com/Maliot100X/clawpump-v2/tree/main/base-skills/tokenized-agents)
- [Wallet Integration Guide](https://raw.githubusercontent.com/pump-fun/pump-fun-skills/refs/heads/main/tokenized-agents/references/WALLET_INTEGRATION.md)
- [Scenario Tests and Troubleshooting](https://raw.githubusercontent.com/pump-fun/pump-fun-skills/refs/heads/main/tokenized-agents/references/SCENARIOS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, environment variable, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied mint address, payment currency, amount, RPC endpoint, and framework before code changes]

## Skill Version(s):

0.1.0 (source: release metadata; SKILL.md frontmatter reports 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
