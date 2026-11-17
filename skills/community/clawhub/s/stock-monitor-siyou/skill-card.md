## Description:

Monitors configured stock symbols and sends Feishu voice alerts when price movement thresholds, limit-up or limit-down checks, or 10-minute amplitude rules trigger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anightmare2](https://clawhub.ai/user/anightmare2)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure recurring stock monitoring for selected A-share, Hong Kong, or U.S. stock symbols and receive Feishu voice alerts when configured thresholds are reached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a neighboring Feishu voice notification script while Feishu and Noiz credentials are available.

Mitigation: Review or pin the Feishu voice notifier dependency before enabling voice alerts, and use dedicated low-privilege Feishu and Noiz credentials.

Risk: Cron execution with broad privileges can expose credentials and increase impact if the script or dependencies are compromised.

Mitigation: Run scheduled monitoring as a dedicated non-root user with only the permissions needed for stock monitoring and notification.

Risk: Cache and log state under shared /tmp paths can be read or modified by other local users on multi-user systems.

Mitigation: Move cache and log files to a private per-user directory with restrictive filesystem permissions.

Risk: Stock alerts depend on external market-data endpoints and simple threshold logic, so alerts can be delayed, missing, or based on unavailable data.

Mitigation: Treat alerts as prompts for review, not financial advice, and verify market data before taking trading action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anightmare2/skills/stock-monitor-siyou)
- [README](artifact/README.md)
- [Skill source description](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime scripts may emit console text and trigger Feishu voice notifications using configured credentials.]

## Skill Version(s):

2.0.0 (source: server release metadata and clawhub.yaml; package.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
