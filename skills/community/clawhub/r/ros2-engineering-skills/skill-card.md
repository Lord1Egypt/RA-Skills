## Description: <br>
Comprehensive ROS 2 engineering guide covering workspace setup, node architecture, communication patterns, lifecycle and component nodes, launch composition, tf2/URDF, ros2_control hardware interfaces, real-time constraints, Nav2, MoveIt 2, perception pipelines, simulation, security, micro-ROS, multi-robot systems, testing, debugging, deployment, and ROS 1 migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbwls99706](https://clawhub.ai/user/dbwls99706) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to design, implement, review, test, debug, and deploy ROS 2 packages, launch files, URDF/xacro assets, DDS configurations, ros2_control integrations, Nav2/MoveIt 2 workflows, simulation setups, and production robotics CI/CD. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples or generated commands may affect real robot motion or host system configuration. <br>
Mitigation: Review commands before execution, test motion-related changes in simulation or staging first, and require operator approval before applying them to physical robots. <br>
Risk: Utility scripts and examples can involve sudo, Docker deployment, boot settings, real-time tuning, rosbag recording, or live telemetry. <br>
Mitigation: Run the smallest necessary command, inspect configuration changes before applying them, and avoid exposing telemetry or DDS traffic on untrusted networks. <br>
Risk: Package scaffolding with overwrite behavior can replace local work. <br>
Mitigation: Keep the workspace in version control and review diffs before using force-style scaffolding options. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dbwls99706/ros2-engineering-skills) <br>
- [README](README.md) <br>
- [Workspace Build](references/workspace-build.md) <br>
- [Nodes and Executors](references/nodes-executors.md) <br>
- [Communication](references/communication.md) <br>
- [Lifecycle Components](references/lifecycle-components.md) <br>
- [Launch System](references/launch-system.md) <br>
- [tf2 and URDF](references/tf2-urdf.md) <br>
- [Hardware Interface](references/hardware-interface.md) <br>
- [Real-time](references/realtime.md) <br>
- [Navigation](references/navigation.md) <br>
- [Manipulation](references/manipulation.md) <br>
- [Perception](references/perception.md) <br>
- [Simulation](references/simulation.md) <br>
- [Security](references/security.md) <br>
- [micro-ROS](references/micro-ros.md) <br>
- [Multi-robot](references/multi-robot.md) <br>
- [Testing](references/testing.md) <br>
- [Debugging](references/debugging.md) <br>
- [Deployment](references/deployment.md) <br>
- [Message Types](references/message-types.md) <br>
- [ROS 1 Migration](references/migration-ros1.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, configuration snippets, review findings, and optional generated files or scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ROS 2 package scaffolding, launch-file analysis, QoS compatibility reports, and distro-aware implementation guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
