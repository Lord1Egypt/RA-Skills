## Description:

Create and manage OpenClaw scheduled tasks for reminders, periodic notifications, and automated workflows using the OpenClaw Cron API or system crontab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chowlee-cc](https://clawhub.ai/user/chowlee-cc)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to create, validate, and troubleshoot one-time reminders, recurring OpenClaw agent tasks, Feishu delivery jobs, and system crontab workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled jobs can persist or run repeatedly at unintended times if cron expressions, time zones, or job IDs are wrong.

Mitigation: Review each cron expression, time zone, job ID, and enablement state before use; validate new jobs with OpenClaw cron list, manual run, and run-history checks.

Risk: Feishu delivery examples can send messages to unintended recipients or include sensitive content.

Mitigation: Review recipient IDs, reply accounts, channels, and message bodies before running examples, and avoid sending sensitive content unless that is intended.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Troubleshooting Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce crontab entries, OpenClaw cron commands, troubleshooting checklists, and small shell scripts.]

## Skill Version(s):

2.1.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
