## Description:

Radar Collision Warning calls a ROS2 radar warning service on a Raspberry Pi through rosbridge WebSocket to retrieve the nearest obstacle distance and report collision warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[33-code](https://clawhub.ai/user/33-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics operators use this skill to query or monitor a Raspberry Pi ROS2 radar collision-warning service from an agent environment. It supports single checks and continuous monitoring that return obstacle distance, warning status, and service errors as JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collision warning output can be unreliable if rosbridge is exposed on an unsafe network or receives untrusted data.

Mitigation: Deploy only in a controlled ROS/Raspberry Pi environment and use network isolation or authenticated transport for rosbridge.

Risk: A non-warning result may be misread as proof that the environment is safe.

Mitigation: Treat non-warning responses as advisory service output, not as a complete safety guarantee.

Risk: Incorrect threshold or interval values can reduce the usefulness of monitoring.

Mitigation: Validate threshold and interval values against the deployment environment before use.

Risk: The startup script can stop matching ROS-related processes.

Mitigation: Review the startup script before running it on a shared or production robot system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/33-code/skills/radar-collision-warning)
- [33-code publisher profile](https://clawhub.ai/user/33-code)
- [radar_collision_warning_node.py](references/radar_collision_warning_node.py)
- [start_radar_rosbridge.sh](references/start_radar_rosbridge.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and a reachable ROS2 rosbridge endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
