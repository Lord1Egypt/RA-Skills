## Description:

交易告警通知 helps agents configure cryptocurrency price, stop-loss/take-profit, and risk alerts with Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading teams use this skill to configure cryptocurrency market alerts and receive Telegram notifications for price movement, stop-loss/take-profit thresholds, and risk signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because it asks for broad local file mutation and shell-command authority.

Mitigation: Review the skill before installing, run it in a constrained agent workspace, and grant file or shell access only for paths and commands needed for the alert workflow.

Risk: Binance credentials could enable more access than the alert workflow requires.

Mitigation: Configure Binance credentials as read-only and do not grant trading or withdrawal permissions.

Risk: Telegram alert messages and chat IDs leave the local environment.

Mitigation: Treat Telegram destinations and alert contents as shared data, avoid secrets in alerts, and confirm what the runtime sends before use.

Risk: The security summary reports inconsistent claims about external writes and data handling.

Mitigation: Assume external data flow is possible until verified, and test with non-sensitive alert data first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/trade-alert)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with JSON examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Binance data-source credentials and Telegram chat or bot configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
