## Description:

Send push notifications through Pushover for reminders, monitoring alerts, cron summaries, and requested out-of-band notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[digitallyborn](https://clawhub.ai/user/digitallyborn)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to send Pushover alerts from OpenClaw workflows, including reminders, monitoring notifications, cron summaries, and notify-me-when tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification content is sent to Pushover, and credentials are required when the command runs.

Mitigation: Use environment variables or a secret manager for the app token and user key, avoid --token and --user command-line arguments, and keep passwords, API keys, personal data, and confidential operational details out of notification messages.

Risk: Emergency priority notifications can repeat until they expire.

Mitigation: Use priority 2 only for urgent alerts and set explicit retry and expire values.

## Reference(s):

- [Pushover API quick reference](references/pushover-api.md)
- [Pushover API documentation](https://pushover.net/api)
- [ClawHub skill page](https://clawhub.ai/digitallyborn/skills/pushover-notify)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON]

**Output Format:** [Markdown instructions with inline shell commands; the bundled script returns a compact JSON success payload.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Pushover app token and user key at runtime; emergency priority requires retry and expire values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
