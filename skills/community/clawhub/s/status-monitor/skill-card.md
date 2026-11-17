## Description:

Manages OpenClaw Agent status upload scripts, periodically syncing agent online status to the cloud monitoring platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yahao333](https://clawhub.ai/user/yahao333)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to configure, run, and manage status uploads from local OpenClaw agents to a hosted dashboard. It supports manual syncs, scheduled execution, daemon operation, interval changes, and service status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a reusable monitoring token and stores it locally.

Mitigation: Prefer MONITOR_PLATFORM_TOKEN or a protected local credentials file, avoid pasting reusable tokens into chat when possible, restrict file permissions, and rotate tokens if exposed.

Risk: The uploader sends OpenClaw agent IDs to a hosted dashboard and can use a configurable monitor URL.

Mitigation: Install only if sending agent identifiers to the dashboard is acceptable, and do not set OPENCLAW_MONITOR_URL or monitorUrl to untrusted endpoints.

Risk: The skill can run a periodic or background uploader from the local machine.

Mitigation: Review before installing, confirm the desired upload interval, monitor logs after enabling, and use the documented stop/status commands to control the service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yahao333/skills/status-monitor)
- [OpenClaw Status Monitor README](README.md)
- [Installation Guide](INSTALL.md)
- [Chinese README](README_cn.md)
- [OpenClaw Agent Monitor Dashboard](https://openclaw-agent-monitor.vercel.app)
- [OpenClaw Agent Monitor Repository](https://github.com/yahao333/openclaw-agent-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service status, upload results, log locations, token setup guidance, and daemon management commands.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
