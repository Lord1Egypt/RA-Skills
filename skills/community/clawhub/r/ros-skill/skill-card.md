## Description: <br>
Controls ROS/ROS2 robots via rosbridge WebSocket CLI for topics, services, nodes, parameters, actions, robot movement, sensor data, and other ROS/ROS2 robot interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lpigeon](https://clawhub.ai/user/lpigeon) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to let an agent inspect, monitor, and control ROS/ROS2 systems through rosbridge. It supports exploration of topics, services, nodes, parameters, actions, sensor streams, and robot movement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move a robot or change robot state through topic publishes, service calls, parameter updates, or action goals. <br>
Mitigation: Use a simulator first, keep the robot area clear, keep an emergency stop available, and require explicit human approval before executing movement, service, parameter, or action commands on real hardware. <br>
Risk: Commands sent to the wrong rosbridge IP or port could affect an unintended ROS/ROS2 system. <br>
Mitigation: Run the connection check first and verify the target IP and port before issuing commands. <br>


## Reference(s): <br>
- [Command Reference](artifact/references/COMMANDS.md) <br>
- [Turtlesim Tutorial](artifact/examples/turtlesim.md) <br>
- [Sensor Monitoring](artifact/examples/sensor-monitor.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lpigeon/ros-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing guidance may lead to ros_cli.py commands; the CLI itself returns JSON and error objects.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
