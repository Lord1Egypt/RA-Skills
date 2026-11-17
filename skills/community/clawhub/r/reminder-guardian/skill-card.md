## Description:

Helps you remember things by keeping a list of reminders, creating the scheduled jobs to alert you, and tracking which ones are done.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-suraj-bhatti](https://clawhub.ai/user/a-suraj-bhatti)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to log reminder requests, produce a ready-to-run OpenClaw cron blueprint, and track reminder status after scheduling or delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder messages and notes may contain private information because they are saved to a local JSON file.

Mitigation: Review the log path and file permissions before use, and avoid storing sensitive reminder text unless the local environment is appropriate.

Risk: Reminders will not run until a user manually creates the OpenClaw cron job from the printed blueprint.

Mitigation: After adding a reminder, review the blueprint, create the cron job with openclaw cron add, and mark the reminder as scheduled only after the job exists.

## Reference(s):

- [Reminder Guardian on ClawHub](https://clawhub.ai/a-suraj-bhatti/skills/reminder-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Text and JSON cron blueprints with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reminder entries are stored in a local JSON log; cron jobs are not created automatically.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
