## Description:

Automates WeCom Smart Sheet workflows by turning natural-language requests into sheet writes, group notifications, local deadline tracking, and scheduled reminders for expense approvals, work tasks, and video production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason918262](https://clawhub.ai/user/jason918262)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to create and track WeCom Smart Sheet records for expense requests, task assignments, and video-production steps, with matching WeCom group notifications and deadline reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive business information through WeCom Smart Sheet and group robot webhooks.

Mitigation: Use it only in a controlled WeCom workspace and require a human confirmation step before sending records or notifications.

Risk: Webhook keys could grant write or notification access if stored in source files or shared prompts.

Mitigation: Keep webhook keys out of source files and provide them through a controlled secret or runtime configuration process.

Risk: Scheduled command-based reminders can send future notifications without another review at send time.

Mitigation: Require confirmation before creating reminders and restrict reminder prompts to the intended WeCom group and record summary.

Risk: The local tracker can store full business records, increasing exposure if the workspace files are shared.

Mitigation: Store only minimal reminder fields such as table, record ID, name, deadline, responsible user, and notification status.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/jason918262/skills/wecom-smartsheet)
- [Skill instructions](artifact/SKILL.md)
- [WeCom Smart Sheet automation helper](artifact/references/wecom_smartsheet.py)
- [WeCom daily deadline check helper](artifact/references/wecom_daily_check.py)
- [Deadline tracker example configuration](artifact/wecom_deadline_tracker.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, Python helper usage, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include WeCom Smart Sheet webhook payloads, group notification content, local tracker updates, and reminder setup instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
