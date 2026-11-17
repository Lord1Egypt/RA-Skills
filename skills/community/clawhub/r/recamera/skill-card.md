## Description:

reCamera (RV1126B) device full-stack Web API reference covering authentication, device management, video/audio/image configuration, recording rules and storage, AI model inference, terminal/logs, and SenseCraft cloud model conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjq2020](https://clawhub.ai/user/mjq2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, debug, and operate integrations with reCamera device HTTP/WebSocket APIs, including authentication, configuration, recording, inference, storage, firmware, and SenseCraft cloud workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through broad device administration and subnet discovery.

Mitigation: Use it only with reCamera devices and subnets the user owns or is explicitly authorized to manage.

Risk: Authenticated workflows require handling device and SenseCraft tokens.

Mitigation: Prefer HTTPS for authenticated traffic and avoid exposing tokens in scripts, logs, browser JavaScript, or shared outputs.

Risk: Documented actions include reboot, factory reset, storage formatting, model deletion, firmware upgrade, and terminal access.

Mitigation: Require explicit user confirmation before any destructive, service-interrupting, firmware-changing, or terminal-access operation.

Risk: Configuration updates can misconfigure a device if partial payloads omit required fields.

Mitigation: Follow the documented read-before-write pattern: fetch the current full configuration, modify only intended fields, and submit the complete updated object.

## Reference(s):

- [API_REFERENCE.md](artifact/API_REFERENCE.md)
- [ClawHub skill page](https://clawhub.ai/mjq2020/skills/recamera)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON, HTTP endpoint examples, and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated API call patterns, device configuration guidance, and structured troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
