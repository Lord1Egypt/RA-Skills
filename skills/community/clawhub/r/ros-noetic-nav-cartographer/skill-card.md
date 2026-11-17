## Description:

ROS Noetic navigation system using Cartographer for localization, interfacing via TF and rosbridge to control move_base for waypoint navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[threelevelchord](https://clawhub.ai/user/threelevelchord)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to operate Cartographer-based ROS Noetic navigation, including pose lookup, waypoint management, and single- or multi-waypoint movement through rosbridge and move_base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One bundled launcher runs code from a different hard-coded skill directory.

Mitigation: Review or fix artifact/scripts/test_pose.sh before installing or running the skill.

Risk: Navigation commands can move a physical robot and are high-impact if waypoints or the ROS setup are wrong.

Mitigation: Use only with a trusted ROS setup, confirm rosbridge is connected to the intended robot, and verify waypoints before issuing goto or cruise commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/threelevelchord/skills/ros-noetic-nav-cartographer)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bash commands plus Python and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted ROS Noetic environment with Cartographer, rosbridge_server, TF, and move_base configured before issuing navigation commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
