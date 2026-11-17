## Description:

Ros1 Noetic General helps agents answer ROS1 Noetic questions and inspect, build, launch, monitor, debug, and stop ROS1 projects across mobile robots, manipulators, perception pipelines, simulation, and OpenClaw integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lljj123](https://clawhub.ai/user/lljj123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for bilingual ROS1 Noetic support, including ROS concepts, catkin workspace checks, launch and runtime diagnostics, motion-control preflights, rosbag workflows, and OpenClaw-to-ROS1 adapter planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lifecycle scripts can read state files and control processes, which may be unsafe if the state file is untrusted or stale.

Mitigation: Review or fix the lifecycle scripts before use and run health or stop commands only against trusted state files created for the current ROS session.

Risk: Motion-control workflows can affect real hardware if ROS command topics are connected to a robot.

Mitigation: Prefer simulation or dry-run inspection first, confirm a working stop path, and require explicit approval before real-hardware motion.

Risk: Rosbridge can expose ROS graph controls across a network boundary.

Mitigation: Expose rosbridge only on trusted networks and define an approved control surface with allowed topics, services, actions, telemetry, and stop behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lljj123/skills/ros1-noetic-general)
- [Official ROS1/Noetic Sources](artifact/references/official-docs.md)
- [ROS1 Noetic Project Profiles](artifact/references/project-profiles.md)
- [ROS1 Engineering Patterns](artifact/references/ros1-engineering-patterns.md)
- [ROS1 Noetic Full Scope](artifact/references/ros1-full-scope.md)
- [OpenClaw to ROS1 Adapter Blueprint](artifact/references/ros1-openclaw-adapter.md)
- [ROS Noetic Documentation](http://docs.ros.org/en/noetic/)
- [ROS Package Index](https://index.ros.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, code snippets, checklists, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run ROS inspection and lifecycle helper scripts when the host environment permits execution.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
