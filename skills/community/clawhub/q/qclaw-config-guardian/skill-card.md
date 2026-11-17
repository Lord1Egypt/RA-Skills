## Description:

QClaw Config Guardian helps an agent back up QClaw/OpenClaw channel, plugin, and cron configuration, check version-related changes, and suggest restoration or repair steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codingduan](https://clawhub.ai/user/codingduan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to preserve QClaw/OpenClaw configuration across upgrades and diagnose missing delivery-channel or target settings in scheduled jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain sensitive channels, plugins, cron jobs, tokens, webhook URLs, private prompts, account IDs, or delivery targets in plaintext.

Mitigation: Run backups intentionally, restrict the backup directory to owner-only access, and delete stale backup files that are no longer needed.

Risk: The documented cron-data handoff uses a fixed temporary path that could expose or mix configuration data on shared systems.

Mitigation: Use a private temporary file or directory with restrictive permissions instead of the fixed /tmp cron-data path.

Risk: Automatic backup and repair flows can preserve or suggest changes to incorrect cron delivery settings.

Mitigation: Review generated health reports and proposed cron updates before applying restoration or repair commands.

## Reference(s):

- [QClaw Config Guardian on ClawHub](https://clawhub.ai/codingduan/skills/qclaw-config-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python script references, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local backup files and JSON health reports when its scripts are executed by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
