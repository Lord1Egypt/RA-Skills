## Description:

Control Tuya smart home devices via natural language, including device control and status queries, home and room management, notifications, weather, statistics, IPC camera captures, and real-time device events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaosq856](https://clawhub.ai/user/gaosq856)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate and inspect Tuya smart-home environments through an agent, including physical device control, monitoring, notifications, camera capture, and related data queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Tuya API key can permit device control, home and device data access, notifications, event monitoring, statistics queries, and camera-media capture.

Mitigation: Use a least-privilege Tuya credential where possible, keep the key out of logs and responses, and only install the skill when that access level is acceptable.

Risk: Physical device actions and camera captures can affect privacy or safety.

Mitigation: Require explicit user confirmation before physical actions or IPC capture, and avoid unattended automation for sensitive devices.

Risk: Endpoint and image-processing disclosures are incomplete in the security evidence.

Mitigation: Restrict endpoints to official Tuya hosts and obtain publisher clarification before sending captured camera media to any AI vision service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaosq856/skills/tuya-smart-control)
- [Tuya Official Website](https://www.tuya.com/)
- [API Conventions](references/api-conventions.md)
- [Device Control](references/device-control.md)
- [Device Query](references/device-query.md)
- [Device Management](references/device-management.md)
- [Home and Space Management](references/home-and-space.md)
- [Device Message Subscription](references/device-message.md)
- [IPC AI Cloud Capture](references/ipc-cloud-capture.md)
- [Notifications](references/notifications.md)
- [Data Statistics](references/statistics.md)
- [Weather Query](references/weather.md)
- [Error Handling](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python examples, JSON payloads, and human-readable status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Tuya API calls, device-control commands, monitoring scripts, and camera-media URLs when authorized.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
