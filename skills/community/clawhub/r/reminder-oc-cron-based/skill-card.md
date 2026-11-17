## Description:

Create, inspect, and cancel OpenClaw cron-based chat reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anghu666](https://clawhub.ai/user/anghu666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to create one-time OpenClaw chat reminders, inspect pending, upcoming, or overdue reminder jobs, and cancel unexecuted reminder jobs. The skill favors the native cron tool workflow and treats the bundled helper script as an optional local convenience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled reminder jobs persist until they run or are removed.

Mitigation: Use the skill only for intended OpenClaw chat reminders, keep ordinary one-time reminders configured to delete after running, and inspect reminder-prefixed jobs before changing them.

Risk: The optional helper script depends on a trusted local OpenClaw binary and correct channel, target, and account routing.

Mitigation: Prefer the native cron tool path when available, and run the helper only in an expected local environment with verified routing variables.

Risk: Ambiguous cancellation requests could target the wrong unexecuted reminder.

Mitigation: List candidate reminder jobs and confirm the exact target before removing a reminder.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, text]

**Output Format:** [Markdown guidance with JSON cron examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs focus on one-shot OpenClaw cron reminder setup, inspection, and cancellation workflows.]

## Skill Version(s):

0.1.0 (source: changelog and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
