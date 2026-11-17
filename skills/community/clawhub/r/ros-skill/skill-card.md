## Description:

Controls ROS/ROS2 robots via rosbridge WebSocket CLI for topics, services, nodes, parameters, actions, robot movement, sensor data, and other ROS/ROS2 interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpigeon](https://clawhub.ai/user/lpigeon)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and robotics engineers use this skill to inspect and control ROS/ROS2 robots through rosbridge, including topic discovery, sensor monitoring, service calls, parameter updates, and robot movement commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad control over real robots and live ROS/ROS2 system state.

Mitigation: Install only for trusted ROS environments and require operator approval before movement commands, action goals, service calls, or parameter writes.

Risk: Movement, service calls, parameter writes, and action goals can move hardware or change robot behavior.

Mitigation: Prefer simulation first, keep an emergency stop available, and stop the robot after movement sequences.

Risk: Exposing rosbridge or this CLI on untrusted networks can create unauthorized control paths.

Mitigation: Avoid untrusted network exposure unless transport security and access controls are added.

## Reference(s):

- [Command Reference](references/COMMANDS.md)
- [Turtlesim Tutorial](examples/turtlesim.md)
- [Sensor Monitoring](examples/sensor-monitor.md)
- [ROS Skill README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use python3, websocket-client, and a reachable rosbridge endpoint; all CLI command results are JSON.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
