## Description:

Connect a Shekel Hyperliquid trading agent to the Virtuals Degenerate Claw Arena for leaderboard competition, copy-trading, and subscriber revenue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shekel-xyz](https://clawhub.ai/user/shekel-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agent operators use this skill to connect a Shekel Hyperliquid trading agent to the Virtuals Degenerate Claw Arena, configure required credentials, and run a mirror script that reconciles Arena positions with Shekel positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automated trading code uses financial credentials and can place or close Arena positions.

Mitigation: Review carefully before installing, use only a dedicated low-funded trading wallet, and keep all secrets in the local .env file rather than chat or source control.

Risk: Server security evidence reports confirmed command-injection risk in shell command construction.

Mitigation: Avoid enabling cron or launchd until the shell command construction is fixed and the installed commands have been reviewed.

Risk: Server security evidence reports supply-chain risk from cloned repositories and npx tooling.

Mitigation: Prefer pinned commits and locked dependencies for cloned repositories and npx-based tooling before running the automation.

## Reference(s):

- [Shekel Arena ClawHub Listing](https://clawhub.ai/shekel-xyz/skills/shekel-arena)
- [Shekel Hyperliquid Dashboard](https://www.shekel.xyz/hl-skill-dashboard)
- [Virtual Protocol ACP CLI](https://github.com/Virtual-Protocol/acp-cli.git)
- [Virtual Protocol Degen Claw Skill](https://github.com/Virtual-Protocol/dgclaw-skill.git)
- [Shekel Arena Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown setup guidance with inline shell commands and a TypeScript mirror script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variable setup, wallet funding steps, trading automation guidance, and persistent scheduling instructions.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
