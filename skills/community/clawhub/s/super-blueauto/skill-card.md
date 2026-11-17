## Description:

Super Blueauto helps agents scan, connect, monitor, and manage local Bluetooth and BLE devices across major operating systems without cloud uploads or data collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephsuo](https://clawhub.ai/user/josephsuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to discover, connect to, inspect, and manage local Bluetooth or BLE devices through natural language workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or disconnect local Bluetooth devices, including locks, health peripherals, shared devices, or production equipment.

Mitigation: Review before installing in sensitive environments, use explicit device names, and require confirmation before writes, on/off commands, or batch disconnects.

## Reference(s):

- [Super Blueauto on ClawHub](https://clawhub.ai/josephsuo/skills/super-blueauto)
- [josephsuo publisher profile](https://clawhub.ai/user/josephsuo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with device-control steps and command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local Bluetooth scan, connection, read, write, and batch-management instructions.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog; artifact Version section says v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
