## Description:

Control Tuya / Smart Life devices locally over LAN: fetch local keys once via the Tuya cloud API, then read and write DPS with tinytuya.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eros5646](https://clawhub.ai/user/eros5646)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home users can retrieve keys for their own Tuya devices, inspect device state, and control devices over a local network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored device keys could expose access to Tuya devices if shared or leaked.

Mitigation: Keep tuya_devices.json out of git and chats, restrict file access, and re-fetch keys if exposed.

Risk: Writing the wrong DPS value could change a physical device unexpectedly.

Mitigation: Control only devices you own; confirm the DPS mapping and value type before writing, then check the resulting device state.

## Reference(s):

- [Tuya Local Control on ClawHub](https://clawhub.ai/eros5646/skills/tuya-local-control)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and JSON status examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local device control requires a device ID, local key, LAN IP, and matching protocol version.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
