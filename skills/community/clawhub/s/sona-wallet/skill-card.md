## Description:

Autonomous Solana wallet agent -- AI reasons, Rust signs. Transfers, swaps, staking, chat, and mode switching under constitutional spend limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neocryptoquant](https://clawhub.ai/user/neocryptoquant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet operators use this skill to let an OpenClaw-compatible agent inspect a local SONA wallet agent, retrieve wallet and policy status, and submit authenticated wallet commands such as transfers, approvals, chat, and mode changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable state-changing wallet actions when SONA_TOKEN is configured, including transfers, approvals, chat-driven actions, and mode changes.

Mitigation: Install only when intentional, protect SONA_TOKEN like a session credential, keep standard or assisted mode unless autonomous execution is deliberate, and review policy limits before using transfer, approve, chat, or god mode.

Risk: A misconfigured service URL could expose wallet session credentials to a remote host.

Mitigation: The plugin restricts SONA_API_URL to localhost-style hosts and falls back to http://localhost:3000 when a remote host is configured.

Risk: Autonomous god mode can execute wallet actions within the configured limits.

Mitigation: Use assisted approvals for sensitive transactions and require the explicit god-mode acknowledgement before enabling autonomous execution.

## Reference(s):

- [SONA homepage](https://www.sonawallet.xyz)
- [ClawHub skill page](https://clawhub.ai/neocryptoquant/skills/sona-wallet)
- [Publisher profile](https://clawhub.ai/user/neocryptoquant)
- [Repository](https://github.com/Ubuntu-Technologies/sona)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-formatted tool responses with setup commands and configuration values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local SONA service; authenticated state-changing actions use SONA_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
