## Description:

Detects basic Spanish and English reminder phrases with HH:MM times and schedules a reminder through Telegram when available or the console otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jul879n](https://clawhub.ai/user/jul879n)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn simple natural-language reminder messages into one-time scheduled notifications in Telegram or a console session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder text may contain sensitive personal information and can be sent back to the same Telegram chat or printed in a shared terminal.

Mitigation: Avoid placing secrets, account details, or highly sensitive content in reminders, especially in shared chats or terminals.

Risk: The skill watches incoming messages for reminder phrases.

Mitigation: Deploy only in contexts where users expect reminder phrase detection and understand where reminder confirmations and notifications are delivered.

## Reference(s):

- [Quick Reminder on ClawHub](https://clawhub.ai/jul879n/skills/quick-reminder)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text reminder and scheduling confirmation messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-time reminders only; accepts basic Spanish and English patterns with HH:MM times.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
