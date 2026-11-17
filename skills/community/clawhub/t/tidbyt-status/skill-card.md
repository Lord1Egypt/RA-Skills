## Description:

Provides an HTTP API that exposes OpenClaw agent status as JSON for Tidbyt LED displays, including status, emoji, activity level, and task counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrscoutshub](https://clawhub.ai/user/mrscoutshub)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to run a local status API and configure a Tidbyt display to show agent activity, task counts, and recent activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unauthenticated status API can expose OpenClaw activity metadata if reachable from an untrusted network.

Mitigation: Bind the API to 127.0.0.1 or a trusted interface, avoid broad firewall rules, and add authentication before LAN or internet exposure.

Risk: Running the API as a background or systemd service can keep the endpoint available longer than intended.

Mitigation: Enable persistence only after deciding how the endpoint will be stopped, monitored, and protected.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mrscoutshub/skills/tidbyt-status)
- [Tidbyt Pixlet releases](https://github.com/tidbyt/pixlet/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, code snippets, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to start or configure a local HTTP API for Tidbyt status display.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
