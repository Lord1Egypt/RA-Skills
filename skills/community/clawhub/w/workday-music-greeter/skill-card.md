## Description:

On weekdays, automatically switches the home-music scene for the current time slot, fetches a matching GIF, and sends a greeting email that embeds and attaches that GIF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users use this skill to automate weekday home-music scene changes and receive scene-matched greeting emails. Developers can customize time slots, GIF queries, recipient settings, and cron scheduling for a local workstation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring weekday cron jobs can repeatedly run user-level automation after installation.

Mitigation: Install only after reviewing the schedule, use dry-run first, and provide or document a clear way to remove the tagged cron entries.

Risk: Editable configuration combined with eval-style shell execution or sourcing .env as shell code can lead to unintended command execution.

Mitigation: Remove eval-style execution, avoid sourcing .env as shell code, quote command arguments directly, and restrict .env file permissions.

Risk: Email delivery depends on local SMTP credentials and a helper script path.

Mitigation: Verify the SMTP helper path and credentials before live use, and keep credentials out of world-readable files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/workday-music-greeter)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Email content, Files]

**Output Format:** [Markdown guidance with bash commands, shell-script output, generated HTML email content, and user crontab entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews; live execution may create temporary GIF or HTML files and install recurring weekday cron entries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
