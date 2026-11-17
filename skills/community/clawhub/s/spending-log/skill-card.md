## Description:

Spending Log helps an OpenClaw agent record personal expenses from natural language, categorize entries, compute monthly spending, check budgets, and generate monthly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baoxinwen](https://clawhub.ai/user/baoxinwen)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to maintain a local personal spending log, query totals by month, category, or date range, receive budget reminders, and generate monthly HTML or CSV expense reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private spending data and can create, edit, delete, export, or back up financial records.

Mitigation: Require explicit user confirmation before write, delete, export, or backup actions, and review destination folders before sharing reports.

Risk: Recurring monthly report delivery can be scheduled through an OpenClaw cron task.

Mitigation: Inspect or disable the scheduled task unless the user has clearly opted in to recurring report generation and delivery.

Risk: Generated reports may be backed up to /volume2/Download/OpenClaw/reports/, which could be shared or synchronized.

Mitigation: Change the backup location or restrict folder permissions when spending data is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baoxinwen/skills/spending-log)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration]

**Output Format:** [Plain text confirmations and summaries, JSON command output, and generated HTML or CSV report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON expense and configuration files; report generation can create local HTML/CSV files and backup copies.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
