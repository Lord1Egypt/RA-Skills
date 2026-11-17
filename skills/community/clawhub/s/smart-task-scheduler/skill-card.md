## Description:

Smart Task Scheduler helps agents import work schedules, manage shift-aware tasks, and calculate adaptive reminders for multi-shift personal schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnkennypan](https://clawhub.ai/user/cnkennypan)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and external users can use this skill to maintain personal work schedules, import Excel or CSV shift tables, update shifts through natural language, and compute reminders that adapt to early, late, split-shift, or rest-day schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent reminder automation can wake the main session and proactively initiate reminders beyond a user's expectations.

Mitigation: Add the cron jobs only after reviewing the schedule, and disable the main-session hourly wake if proactive reminders are not required.

Risk: The skill handles Feishu credentials and personal schedule or task data.

Mitigation: Use least-privilege Feishu app credentials, store schedule files in a dedicated workspace path, and avoid exposing those files or secrets in shared repositories.

Risk: Imported schedules or natural-language updates can produce incorrect reminder times if shift data is wrong or ambiguous.

Mitigation: Confirm imported and updated schedules with the schedule display command and review calculated reminders before relying on alerts.

## Reference(s):

- [Smart Task Scheduler on ClawHub](https://clawhub.ai/cnkennypan/skills/smart-task-scheduler)
- [Publisher profile: cnkennypan](https://clawhub.ai/user/cnkennypan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples, schedule tables, and JSON-shaped schedule/task examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cron setup commands and guidance for Feishu environment variables and workspace schedule/task files.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
