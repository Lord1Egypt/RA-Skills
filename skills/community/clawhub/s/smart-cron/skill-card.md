## Description:

Schedule and manage OpenClaw tasks using natural language with timezone support, failure alerts, logs, and cron lifecycle commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Smart Cron to schedule recurring OpenClaw tasks in plain English, manage those jobs over their lifecycle, and inspect next-run times and execution logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled OpenClaw tasks may continue running unattended after creation.

Mitigation: Review each schedule before enabling it, and use pause, resume, and remove commands to control active jobs.

Risk: Local job logs may contain task names, outputs, or error details from sensitive work.

Mitigation: Use the configured log-retention setting and avoid scheduling tasks that write sensitive content to persistent logs unless retention is acceptable.

Risk: WhatsApp or Telegram failure alerts may expose task names and error details to configured channels.

Mitigation: Configure alert channels carefully and avoid including sensitive information in scheduled task names or alert-visible outputs.

## Reference(s):

- [Smart Cron ClawHub Skill Page](https://clawhub.ai/mariusfit/skills/smart-cron)
- [Smart Cron Source](https://github.com/mariusfit/smart-cron)
- [Smart Cron Issues](https://github.com/mariusfit/smart-cron/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cron lifecycle commands, schedule examples, timezone configuration, alert setup guidance, and log inspection guidance.]

## Skill Version(s):

1.0.0 (source: release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
