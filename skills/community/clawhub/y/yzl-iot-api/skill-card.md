## Description:

yzl-iot-api is a deprecated YZL IoT device management skill that reads soil and liquid-level sensor data and sends remote water-valve control commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzlkj](https://clawhub.ai/user/yzlkj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent query YZL IoT devices for sensor readings, device status, and recent history, or issue explicit commands to supported remote water valves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open or close real-world water valves from broad natural-language commands without an explicit confirmation or device-specific selection.

Mitigation: Use it only where valve commands are deliberate, prefer explicit manual commands with device IDs, and require human confirmation before sending control commands.

Risk: The skill requires access to YZLIOT_API_KEY, which can authorize IoT device reads and control actions.

Mitigation: Limit access to the environment variable, rotate the key when exposure is suspected, and run the skill only in trusted workspaces.

Risk: Each run may check ClawHub for version information.

Mitigation: Use it in environments where periodic version-check network access to ClawHub is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzlkj/skills/yzl-iot-api)
- [ClawHub publisher profile](https://clawhub.ai/user/yzlkj)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text command output with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the YZLIOT_API_KEY environment variable; tool output may include device status, sensor values, command results, errors, and migration notices.]

## Skill Version(s):

1.5.0 (source: server release metadata, artifact _meta.json, and local tool version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
