## Description:

Automated work log management with daily and weekly report generation for recording tasks, tracking progress, setting reminders, and updating completion status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwl52](https://clawhub.ai/user/wwl52)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to keep local work logs, update task progress, receive reminders for unfinished tasks, and generate daily or weekly status reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local work notes can include secrets, credentials, or sensitive business details.

Mitigation: Avoid entering secrets or highly sensitive details, and review or delete stored logs when they are no longer needed.

Risk: Recurring reminders for unfinished tasks can continue until task status is updated.

Mitigation: Mark tasks complete, update progress, or delete stale log entries to stop unnecessary reminders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwl52/skills/work-log)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Conversational text and Markdown reports, with local JSON work-log entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered work notes locally under ~/.workbuddy/work-log/logs.json.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
