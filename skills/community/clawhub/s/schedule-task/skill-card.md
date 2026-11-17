## Description:

Schedule and run recurring tasks on Linux/Unix systems. Use when user wants to set up cron jobs, scheduled backups, periodic data sync, automated reports, or any recurring task automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to create, list, remove, enable, disable, and inspect recurring cron-based tasks such as backups, sync jobs, and automated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent cron jobs that continue running after an agent session ends.

Mitigation: Review each proposed schedule and command before installation, and use a disposable or well-backed-up account for testing.

Risk: The implementation may overwrite existing cron jobs or fail to remove the last scheduled job.

Mitigation: Back up the existing crontab before use and require changes that preserve non-skill cron entries and clearly mark skill-managed lines.

Risk: Scheduled-task text may be unsafe if untrusted commands, paths, or log destinations are accepted without validation.

Mitigation: Validate task fields, prefer absolute paths, test commands manually, and require confirmation before modifying crontab.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/schedule-task)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose cron expressions and crontab-changing shell commands for review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
