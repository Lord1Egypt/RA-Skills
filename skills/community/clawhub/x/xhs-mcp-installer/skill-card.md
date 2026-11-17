## Description:

Installs and starts the Xiaohongshu MCP service on macOS or Linux by detecting the platform, downloading the service binary, configuring autostart, and validating service health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexduming](https://clawhub.ai/user/alexduming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up a local Xiaohongshu MCP service, keep it running in the background, and check login status before connecting an MCP client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer configures persistent background service behavior through launchd or systemd and may add watchdog recovery.

Mitigation: Review the service configuration before installation, run the service as an unprivileged user where possible, and disable autostart or watchdog behavior if persistence is not intended.

Risk: The installer downloads and runs release binaries from GitHub, including latest-release paths that may change over time.

Mitigation: Use a pinned, verified release and inspect the installer and downloaded artifact before execution.

Risk: The cookie import path can store browser cookies that may function as account credentials.

Mitigation: Prefer QR-code login when possible; avoid importing cookies unless necessary, and protect any generated cookies.json with restrictive local file permissions.

Risk: Process cleanup, port handling, cron edits, and service setup could affect unrelated local processes or scheduled jobs.

Mitigation: Review the commands for port 18060, process termination, crontab filtering, and service paths before allowing the skill to run them.

## Reference(s):

- [Xiaohongshu MCP GitHub repository](https://github.com/xpzouying/xiaohongshu-mcp)
- [ClawHub skill page](https://clawhub.ai/alexduming/skills/xhs-mcp-installer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The guidance may create local service files, watchdog scripts, logs, QR-code image output, and cookies.json during setup.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
