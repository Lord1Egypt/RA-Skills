## Description:

Create, edit, validate, and manage KNX Gateway automation workflows and scenes through a REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmpbin](https://clawhub.ai/user/tmpbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, smart-home operators, and automation engineers use this skill to discover KNX devices, create scenes, generate importable workflows, validate configurations, and manage workflow lifecycle through a user-provided KNX Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable persistent automations and perform high-impact smart-home actions.

Mitigation: Require explicit confirmation before deletes, lock, garage, window, scene execution, workflow enablement, webhook exposure, or HTTP/MQTT/email destination changes.

Risk: The gateway access pattern uses a bearer token and may default to plaintext HTTP.

Mitigation: Use a secret store for KNX_TOKEN, prefer HTTPS or an encrypted tunnel, connect only on a trusted LAN or VPN, and use a least-privilege token if supported.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tmpbin/skills/ycznwl-smarthome)
- [Source Homepage](https://github.com/tmpbin/knx-gateway-skills)
- [API Reference](ref/api.md)
- [Device Reference](ref/devices.md)
- [Scene Reference](ref/scenes.md)
- [Trigger Reference](ref/triggers.md)
- [Node Reference](ref/nodes.md)
- [Workflow Examples](ref/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST API requests and JSON scene or workflow payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device-control actions, workflow import JSON, scene definitions, validation steps, and token-handling guidance.]

## Skill Version(s):

1.0.6 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
