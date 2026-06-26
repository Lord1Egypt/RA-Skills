## Description: <br>
Control Tuya smart home devices via natural language, including device control and status queries, home and room management, notifications, weather, data statistics, IPC camera capture, and real-time device events via WebSocket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaosq856](https://clawhub.ai/user/gaosq856) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate Tuya smart-home devices, query device state, send self-notifications, inspect home data, and monitor device events. It is intended for users who explicitly want agent access to Tuya devices and camera capture workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Tuya API key that can control smart-home devices and access account data. <br>
Mitigation: Protect TUYA_API_KEY, avoid printing it in logs or chat output, and install the skill only where Tuya device control is intended. <br>
Risk: Camera capture and visual analysis can expose private media outside the user's expected context. <br>
Mitigation: Require explicit approval before camera capture or AI image analysis, and explain when decrypted image or video URLs will be used. <br>
Risk: A user-supplied TUYA_BASE_URL could redirect API calls to an untrusted endpoint. <br>
Mitigation: Use automatic region detection where possible and override TUYA_BASE_URL only for trusted Tuya endpoints. <br>
Risk: Broad WebSocket monitoring or automations can observe or act on many devices. <br>
Mitigation: Scope monitoring and automations to specific devices and apply notification throttling for event-driven alerts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gaosq856/tuya-smart-control) <br>
- [Tuya Official Website](https://www.tuya.com/) <br>
- [API Conventions](references/api-conventions.md) <br>
- [Device Control](references/device-control.md) <br>
- [Device Query](references/device-query.md) <br>
- [Device Message Subscription](references/device-message.md) <br>
- [IPC AI Cloud Capture](references/ipc-cloud-capture.md) <br>
- [Notifications](references/notifications.md) <br>
- [Error Handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands or scripts that call Tuya APIs and may return smart-home device status, notification results, event-monitoring guidance, or camera capture URLs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
