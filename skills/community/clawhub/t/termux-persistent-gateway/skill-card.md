## Description:

Keeps an AI agent gateway running persistently on Android/Termux using tmux, wake-lock, Termux:Boot, and health monitoring without systemd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofqin2026](https://clawhub.ai/user/kingofqin2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep a trusted gateway process running on Android/Termux, including after screen-off, app switching, and device reboot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A gateway configured for boot or cron persistence can continue running after reboot or in the background when the user no longer expects it.

Mitigation: Enable boot and cron persistence only for a trusted gateway, document the Termux:Boot script and cron entry, and remove them when persistence is no longer needed.

Risk: An incorrect GATEWAY_CMD or SCRIPT path can start the wrong command or fail repeated health checks.

Mitigation: Review and test GATEWAY_CMD, SESSION_NAME, LOG_DIR, and SCRIPT_PATH before enabling health monitoring or boot startup.

Risk: A long-running gateway may expose network services or consume device resources.

Mitigation: Restrict network exposure, monitor logs and resource use, and disable the tmux session and wake-lock when the gateway should stop.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingofqin2026/skills/termux-persistent-gateway)
- [Artifact README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, persistence, health-check, logging, and troubleshooting guidance for a Termux gateway.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
