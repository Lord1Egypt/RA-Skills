## Description:

A ROS 2 engineering skill that guides agents through workspace setup, node architecture, communication, lifecycle components, launch files, simulation, security, testing, debugging, deployment, and ROS 1 migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbwls99706](https://clawhub.ai/user/dbwls99706)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to have an agent generate, review, debug, and deploy ROS 2 code, packages, launch files, URDF/xacro, DDS/QoS configuration, and fleet-oriented robotics workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes setup examples that can run privileged Docker, system tuning, or pipe-to-shell installation commands.

Mitigation: Review and adapt those commands before execution, avoid pipe-to-shell installation, and require operator approval for privileged or host-modifying commands.

Risk: The package generator has an input-validation flaw for maintainer metadata.

Mitigation: Do not pass untrusted maintainer metadata to scripts/create_package.py unless validation is added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dbwls99706/skills/ros2-engineering-skills)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Workspace Build](artifact/references/workspace-build.md)
- [Nodes and Executors](artifact/references/nodes-executors.md)
- [Communication](artifact/references/communication.md)
- [Lifecycle Components](artifact/references/lifecycle-components.md)
- [Launch System](artifact/references/launch-system.md)
- [TF2 and URDF](artifact/references/tf2-urdf.md)
- [Hardware Interface](artifact/references/hardware-interface.md)
- [Realtime](artifact/references/realtime.md)
- [Navigation](artifact/references/navigation.md)
- [Manipulation](artifact/references/manipulation.md)
- [Perception](artifact/references/perception.md)
- [Simulation](artifact/references/simulation.md)
- [Security](artifact/references/security.md)
- [micro-ROS](artifact/references/micro-ros.md)
- [Multi-Robot](artifact/references/multi-robot.md)
- [Testing](artifact/references/testing.md)
- [Debugging](artifact/references/debugging.md)
- [Deployment](artifact/references/deployment.md)
- [Message Types](artifact/references/message-types.md)
- [ROS 1 Migration](artifact/references/migration-ros1.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code blocks, shell commands, configuration examples, and file-level recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend executing generated or referenced commands; review commands before use in privileged, networked, or production robot environments.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
