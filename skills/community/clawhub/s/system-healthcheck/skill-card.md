## Description:

Three-tier system health monitoring (L1/L2/L3) with heartbeat mechanism. Zero external dependencies, i18n support, console output only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lim1202](https://clawhub.ai/user/lim1202)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw host health through fast file checks, hourly resource, service, and log checks, daily audits, and heartbeat status output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring host execution can inspect local OpenClaw files, process and service state, logs, package-update status, and temporary or cache directories.

Mitigation: Review scripts and crontab entries before enabling schedules, run without elevated privileges, and remove cron entries to disable recurring checks.

Risk: Configuration controls may not fully stop scheduled checks after cron entries are installed.

Mitigation: Treat crontab as the authority for recurring execution and remove or comment scheduled entries when disabling the skill.

Risk: Healthcheck output can reveal local system state and log details.

Mitigation: Write output only to intended local consoles or logs and limit access to generated healthcheck logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lim1202/skills/system-healthcheck)
- [README.md](README.md)
- [INSTALL.md](INSTALL.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional console or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Console-oriented health status output; documented script modes include quiet output and JSON output.]

## Skill Version(s):

1.0.1 (source: server release metadata and CHANGELOG, released 2026-03-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
