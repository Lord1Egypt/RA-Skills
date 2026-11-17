## Description:

Monitor remote servers via SSH — check service health (PM2, systemd, Docker), database status (MongoDB, MySQL, PostgreSQL), disk space, memory, and auto-restart crashed services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qoohsuan](https://clawhub.ai/user/qoohsuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to inspect server health, diagnose service or database outages, propose restart commands, and set up MongoDB watchdog monitoring on servers they administer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide persistent service restarts and deploy a watchdog that restarts MongoDB automatically.

Mitigation: Use it only on servers you administer, review restart commands before execution, and require explicit approval before enabling persistent PM2 deployment or automatic restarts.

Risk: The watchdog may send MongoDB crash details to Telegram and includes a hard-coded chat ID and host-specific values.

Mitigation: Remove host-specific defaults, configure alert destinations explicitly through environment variables or local configuration, and disable outbound alerts unless they are approved.

Risk: The skill documents password-based SSH with relaxed host-key checking.

Mitigation: Prefer key-based SSH, verify host keys, and avoid embedding or transmitting passwords in generated commands.

Risk: The deployment recipe installs dependencies without a lockfile.

Mitigation: Pin and review dependencies with a lockfile before deploying the watchdog service.

## Reference(s):

- [Server Watchdog ClawHub page](https://clawhub.ai/qoohsuan/skills/server-watchdog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service restart steps, health-check commands, alert templates, and watchdog deployment guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
