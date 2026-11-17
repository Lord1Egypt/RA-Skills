## Description:

Monitors A-share T+0 funds at a five-minute cadence, maintains a watchlist, calculates technical indicators, and surfaces informational buy/sell signals with optional terminal, DingTalk, or WeCom notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newhackerman](https://clawhub.ai/user/newhackerman)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to add or remove fund codes, run a China-market T+0 fund monitor, and review generated technical trading signals. The signals are informational only and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading signals can influence financial decisions while relying on unauthenticated or delayed third-party market data.

Mitigation: Treat alerts as untrusted informational signals, verify market data independently, and require human review before any trade.

Risk: Configured DingTalk or WeCom webhooks may receive fund codes, prices, signal reasons, and confidence values.

Mitigation: Review webhook settings before enabling notifications, restrict webhook access, rotate tokens when exposed, and leave unused channels disabled.

Risk: The skill stores watchlists and simulated trade history locally.

Mitigation: Review local data paths and permissions, disclose retention expectations to users, and clear stored data when it is no longer needed.

Risk: Installer and cleanup scripts modify local skill directories, install Python packages, and delete monitor data files.

Mitigation: Review scripts before execution, avoid running them as root, and prefer pinned dependencies and HTTPS-only data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newhackerman/skills/t0-fund-monitor)
- [Publisher profile](https://clawhub.ai/user/newhackerman)
- [OpenClaw skills homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style CLI guidance with shell commands, YAML configuration examples, terminal notifications, and JSON-backed signal or trade records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signals depend on delayed third-party market data and are intended for human review before any trading decision.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
