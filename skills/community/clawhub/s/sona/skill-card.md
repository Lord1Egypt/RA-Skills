## Description:

Autonomous Solana wallet agent that supports transfers, swaps, staking, chat, and mode switching under constitutional spend limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neocryptoquant](https://clawhub.ai/user/neocryptoquant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external wallet operators use this skill to connect OpenClaw-compatible agents to a local SONA Solana wallet dashboard for status checks, policy inspection, chat, transfers, queued approvals, and mode changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An OpenClaw agent with SONA_TOKEN can move funds, approve queued wallet actions, send arbitrary wallet-agent commands, and switch SONA into autonomous mode.

Mitigation: Use devnet or low-value wallets, keep policy limits tight, and expose SONA_TOKEN only to trusted agents and contexts.

Risk: The skill has high-impact wallet-control authority without strong confirmation boundaries.

Mitigation: Review the skill before deployment and require human review before enabling modes or workflows that can execute fund-moving actions.

## Reference(s):

- [Sona Agentic Wallet on ClawHub](https://clawhub.ai/neocryptoquant/skills/sona)
- [SONA homepage](https://www.sonawallet.xyz)
- [SONA repository](https://github.com/Ubuntu-Technologies/sona)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration, Guidance]

**Output Format:** [Markdown or plain text returned from wallet and agent tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool output can include wallet status, SOL price, policy details, activity summaries, pending actions, chat responses, and transaction or approval results.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
