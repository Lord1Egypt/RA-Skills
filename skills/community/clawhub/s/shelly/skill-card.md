## Description:

Control and automate Shelly devices with local RPC workflows, secure access modes, cloud API coordination, and safe multi-device execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, operators, and smart-home maintainers use this skill to inspect, control, and orchestrate Shelly devices across local RPC, WebSocket, MQTT, and cloud-assisted workflows with explicit safety gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-assisted Shelly writes can affect relays, heating, locks, alarms, or multiple devices if execution boundaries are unclear.

Mitigation: Begin in read-only inspection mode, require explicit confirmation before high-impact or bulk actions, use canary-first rollout, and verify device state after each write.

Risk: Shelly cloud credentials could be exposed if users paste tokens into chat or store them in notes.

Mitigation: Read SHELLY_CLOUD_TOKEN from environment variables, avoid raw secrets in local notes, and keep credentials scoped to the intended operations.

Risk: Local and cloud control views can diverge, causing conflicting state decisions or duplicate writes.

Mitigation: Select the control plane before acting, reconcile device identity when views differ, and prefer local device state for immediate decisions when reachable.

## Reference(s):

- [ClawHub Shelly Skill](https://clawhub.ai/ivangdavila/skills/shelly)
- [Shelly Skill Homepage](https://clawic.com/skills/shelly)
- [Shelly API Documentation](https://shelly-api-docs.shelly.cloud)
- [Setup - Shelly](artifact/setup.md)
- [Shelly Access and Authentication](artifact/auth-and-access.md)
- [Shelly Device Operations Workflow](artifact/device-operations.md)
- [Shelly Protocol and Transport Matrix](artifact/protocol-matrix.md)
- [Shelly Orchestration Playbooks](artifact/orchestration-playbooks.md)
- [Shelly Troubleshooting and Recovery](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, operational checklists, and Shelly RPC/API payload guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cloud workflows require SHELLY_CLOUD_TOKEN from the environment; examples assume curl and jq are available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
