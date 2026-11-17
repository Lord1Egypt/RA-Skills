## Description:

Capture natural-language events in Chinese or English, save them to the user's OpenClaw workspace, and schedule Telegram reminders with default 24-hour, 1-hour, and 10-minute notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to turn natural-language meeting, birthday, deadline, and planning requests into stored reminder events and scheduled Telegram notifications. It also helps users query upcoming plans from their reminder workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder details are saved in the user's OpenClaw workspace and may contain personal schedule information.

Mitigation: Install only if local workspace storage of reminder details is acceptable, and keep machine-specific secrets out of committed files.

Risk: Incorrect timezone settings or ambiguous natural-language dates can schedule reminders at the wrong time.

Mitigation: Set REMINDER_TZ when not using Asia/Shanghai, ask minimal clarifying questions for ambiguous dates, and verify important reminder times after scheduling.

Risk: Telegram reminder jobs may continue sending outdated notifications if changed events are not reconciled.

Mitigation: Confirm cancellations or changes and remove or replace related cron jobs when reminder events are edited.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fresh3/skills/taizi-reminder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Concise natural-language replies with workspace event updates and cron scheduling instructions or actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses REMINDER_TZ and REMINDER_OFFSETS_MINUTES to control timezone and default notification offsets.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact _meta.json reports 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
