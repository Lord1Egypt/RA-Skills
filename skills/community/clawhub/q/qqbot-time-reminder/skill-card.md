## Description:

创建每分钟发送当前时间的QQ定时提醒任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric331](https://clawhub.ai/user/eric331)

### License/Terms of Use:

MIT-0

## Use Case:

QQ bot users can use this skill to create a scheduled reminder that sends the current time every minute. It is also suitable for testing OpenClaw cron task creation and cancellation behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a persistent QQ messaging task that sends every minute and may continue until explicitly removed.

Mitigation: Use it only when a continuing every-minute reminder is intended, keep the returned task ID, and remove the cron job when the reminder is no longer needed.

Risk: A wrong recipient OpenID or timezone can send repeated reminders to the wrong destination or at an unexpected local time.

Mitigation: Confirm the recipient OpenID and Asia/Shanghai timezone before creating the cron task.

Risk: The artifact says the skill may be used for hourly time reports, but its cron expression runs every minute.

Mitigation: For hourly reminders, correct the cron schedule before creating the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eric331/skills/qqbot-time-reminder)
- [Publisher profile](https://clawhub.ai/user/eric331)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or removes an OpenClaw cron task for QQ bot delivery; returns the task ID and cancellation guidance when a reminder is created.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
