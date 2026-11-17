## Description:

Work Schedule Assistant stores work arrangements, meetings, to-dos, and related attachments in a persistent local schedule ledger and generates daily reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liqiang12689](https://clawhub.ai/user/liqiang12689)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to turn work chat messages into a persistent local schedule ledger, manage items and attachments, and generate daily reminders for today's work, overdue items, and unscheduled tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Work messages, notes, history, and selected attachments are stored persistently on the user's machine.

Mitigation: Install only when persistent local storage is desired, avoid saving secrets or highly sensitive documents, and use the documented data directory controls.

Risk: Daily reminders require cron setup and may post schedule summaries to a configured channel.

Mitigation: Review cron configuration before approval and confirm the channel, recipient, and timezone match the intended delivery target.

Risk: Links or Markdown content from untrusted messages may be displayed in the schedule ledger.

Mitigation: Be cautious with untrusted links or Markdown content and review generated ledger entries before relying on them.

## Reference(s):

- [Attachment Handling](references/attachment-handling.md)
- [Daily Reminder Setup](references/setup-reminder.md)
- [ClawHub Skill Page](https://clawhub.ai/liqiang12689/skills/work-schedule-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Text confirmations, Markdown ledgers, JSON schedule/history files, and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local schedule data and optional copied attachments under the configured work-schedule directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
