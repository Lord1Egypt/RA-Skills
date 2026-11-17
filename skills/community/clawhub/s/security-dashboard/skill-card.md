## Description:

Security Dashboard provides real-time monitoring for OpenClaw and Linux server security, including gateway status, network exposure, system updates, SSH access, TLS certificates, and resource usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vegasbrianc](https://clawhub.ai/user/vegasbrianc)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure operators use this skill to install and operate a local dashboard that monitors OpenClaw and Linux server security posture through web UI metrics, alerts, and service commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer grants broader passwordless sudo access than the documentation makes clear.

Mitigation: Review scripts/install.sh before installation, prefer the dedicated dashboard user over root, and replace wildcard sudoers entries with narrow, root-owned metrics helpers.

Risk: The web server has file disclosure risk.

Mitigation: Keep the dashboard bound to 127.0.0.1 and fix static file traversal handling before any administrator-facing deployment.

Risk: The dashboard has injection risk from rendered metric or alert content.

Mitigation: Sanitize dashboard data and replace unsafe innerHTML rendering before exposing the dashboard to administrators.

## Reference(s):

- [ClawHub Security Dashboard Listing](https://clawhub.ai/vegasbrianc/skills/security-dashboard)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local system state and service commands for dashboard installation, monitoring, and risk review.]

## Skill Version(s):

1.2.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
