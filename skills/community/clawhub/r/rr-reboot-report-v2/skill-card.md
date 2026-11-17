## Description:

Detect unexpected system reboots, alert when the system comes back online, track boot history, and flag suspicious restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elony-7](https://clawhub.ai/user/elony-7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and administrators use this skill to check whether a system rebooted unexpectedly, inspect boot history, and set up Telegram reboot alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram alerting sends reboot notifications to an external service when enabled.

Mitigation: Install the alert path only on systems where Telegram reboot notifications are intended, and review the cron entry before enabling it.

Risk: Telegram credentials are read from ~/.rr-reboot-config.

Mitigation: Use a dedicated low-privilege Telegram bot, restrict the config file permissions, and avoid sharing the config file.

Risk: The bot token may be visible in process arguments while the alert command runs.

Mitigation: Harden the script before relying on it in shared or monitored environments, or run it only where process argument exposure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elony-7/skills/rr-reboot-report-v2)
- [Publisher profile](https://clawhub.ai/user/elony-7)
- [Telegram Bot API endpoint](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The check script can emit plain-text status lines or JSON when invoked with --json.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
