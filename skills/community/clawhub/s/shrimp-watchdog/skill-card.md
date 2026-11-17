## Description:

Keep OpenClaw gateway alive with heartbeat monitoring, auto-restart, crash alerts, memory warnings, uptime reports, and configurable port monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarrymo](https://clawhub.ai/user/sarrymo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor an OpenClaw Gateway service, check process and port health, restart it when unavailable, and report operational status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged watchdog behavior may automatically restart openclaw-gateway through systemd.

Mitigation: Require explicit operator confirmation for restart-capable monitoring and scope service permissions narrowly before deployment.

Risk: The release references a watchdog script path but does not bundle an auditable watchdog.sh implementation.

Mitigation: Review the actual watchdog.sh before use and require strict validation for configurable port, interval, and threshold parameters.

Risk: The authoritative security review marks this release suspicious because it directs a privileged systemd watchdog to automatically restart openclaw-gateway without a bundled, auditable implementation or tight controls.

Mitigation: Follow the security guidance in evidence.json before installation, including auditable implementation review and tight operational controls.

## Reference(s):

- [OpenClaw Watchdog on ClawHub](https://clawhub.ai/sarrymo/skills/shrimp-watchdog)
- [sarrymo publisher profile](https://clawhub.ai/user/sarrymo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and operational status/report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce monitoring instructions, restart guidance, alert text, and uptime report content for an OpenClaw Gateway watchdog.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
