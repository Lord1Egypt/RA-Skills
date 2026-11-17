## Description:

Upbit automated trading (aggressive breakout) with cron-friendly run-once commands, TopVolume monitoring, and percent-based budget splitting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuns9](https://clawhub.ai/user/kuns9)

### License/Terms of Use:

ISC

## Use Case:

External users and developers use this skill to monitor Upbit KRW markets, generate trading signals, and run cron-friendly monitor and worker commands that can place or simulate orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unattended real Upbit trades and may manage existing account holdings.

Mitigation: Review before installing, use dry-run first, restrict API key permissions and funds, and verify whether managing existing holdings is intended.

Risk: Safety documentation and sizing controls are reported as inconsistent for percent-based budget splitting.

Mitigation: Do not rely on the documented percent-based budget split until the implementation is fixed or independently confirmed.

Risk: Live deployment depends on third-party packages without a lockfile in the artifact evidence.

Mitigation: Pin dependencies and use a lockfile before live deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kuns9/skills/trading-upbit-skill)
- [Upbit API base URL](https://api.upbit.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create and update local JSON state files for events, positions, cached market data, and heartbeats when run.]

## Skill Version(s):

1.0.14 (source: ClawHub release metadata; artifact package/frontmatter report 13.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
