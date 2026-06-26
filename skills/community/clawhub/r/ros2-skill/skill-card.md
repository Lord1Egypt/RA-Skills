## Description: <br>
Controls and monitors ROS 2 robots directly via rclpy CLI for topics, services, actions, parameters, nodes, lifecycle management, controllers, diagnostics, battery status, system health checks, and related ROS 2 operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adityakamath](https://clawhub.ai/user/adityakamath) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, robotics engineers, and external agent operators use this skill to let an AI agent inspect, configure, and operate ROS 2 robots through a structured rclpy command interface. It supports live graph discovery, robot motion workflows, diagnostics, package inspection, launch and run management, component control, and emergency stop handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad live-robot control, including motion, controller changes, process launches, and emergency stop behavior. <br>
Mitigation: Install only in a controlled ROS 2 environment where the operator expects agent control of hardware, and require human confirmation for motion, controller changes, process launches, and any other hardware-affecting action. <br>
Risk: The skill can manage persistent ROS 2 launch, run, and component sessions. <br>
Mitigation: Review active sessions before and after use, route session termination through the documented command groups, and require confirmation before starting or killing long-running robot processes. <br>
Risk: The release includes a Discord workflow that can send files outside the robot environment. <br>
Mitigation: Review the Discord workflow before use, restrict or remove bot-token access if external sharing is not required, and require human confirmation for file upload. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adityakamath/ros2-skill) <br>
- [README](README.md) <br>
- [CLI Reference](references/CLI.md) <br>
- [Command Reference](references/COMMANDS.md) <br>
- [Examples](references/EXAMPLES.md) <br>
- [Rules](references/RULES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to be run through scripts/ros2_cli.py and return JSON; the skill requires python3, ros2, rclpy, and a sourced ROS 2 environment.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and changelog, released 2026-03-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
