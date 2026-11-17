## Description:

Manages QQBot reminders through real OpenClaw cron jobs with explicit per-user timezone settings for reminders, alarms, timed notifications, recurring reminders, lookup, cancellation, and timezone changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zykkk-power](https://clawhub.ai/user/zykkk-power)

### License/Terms of Use:

MIT-0

## Use Case:

QQBot operators and agents use this skill to set user timezones and create, list, or cancel one-shot and recurring QQ reminders backed by OpenClaw cron jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent OpenClaw cron jobs for QQ reminders.

Mitigation: Review reminder target, timezone, and recurrence before scheduling, and periodically list active jobs to remove reminders that are no longer needed.

Risk: Cancellation by job ID may be too broad in shared or multi-user environments.

Mitigation: Confirm that a job belongs to the requesting QQ target before removing it, or add ownership checks around cancellation.

Risk: Scheduled reminder agents could run with broader access than the reminder task requires.

Mitigation: Run scheduled reminders with minimal tools and without access to sensitive files or credentials.

## Reference(s):

- [Artifact reference notes](references.txt)
- [ClawHub skill page](https://clawhub.ai/zykkk-power/skills/qqbot-remind-absolute)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and manages persistent OpenClaw cron jobs for QQ reminder delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
