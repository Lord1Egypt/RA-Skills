## Description:

Splits a tagged weekly work plan into five weekday Markdown daily plans and supports recurring OpenClaw jobs for weekly copying, Sunday splitting, and Feishu daily-plan delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seairteng](https://clawhub.ai/user/seairteng)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to convert a structured weekly project plan into weekday daily plans, track completed checklist items, and prepare recurring plan notifications. It is intended for users who explicitly want automated local plan-file management and optional Feishu delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring OpenClaw jobs can continue reading business plan files and sending full daily-plan contents through Feishu without fresh confirmation.

Mitigation: Enable cron only after confirming the plan directories, Feishu destination, retention expectations, and the exact remove or pause procedure for all three jobs.

Risk: Daily plans may include customer names, project deadlines, locations, responsible people, and notes that could be sensitive if forwarded externally.

Mitigation: Use only approved internal Feishu destinations, keep webhook access controlled, and limit automated delivery to non-sensitive daily-plan content.

Risk: The automation writes and updates plan files, so an incorrect path or malformed plan format can affect the wrong files or produce unusable daily plans.

Mitigation: Verify the configured plan directories and file naming format, run dry-run validation before scheduled execution, and keep backups for files managed by the automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seairteng/skills/week-to-day-splitter)
- [Artifact Skill Instructions](artifact/SKILL.md)
- [Artifact Privacy Cleanup Notes](artifact/README.md)
- [Artifact Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown daily-plan files with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local weekly and daily plan files; configured cron jobs may read and send full daily-plan contents through Feishu.]

## Skill Version(s):

1.1.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
