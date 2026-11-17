## Description:

Connects to ROS Noetic navigation through rosbridge to read maps, manage waypoints, send single-goal navigation commands, and run multi-waypoint cruises for AMCL-localized robots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[threelevelchord](https://clawhub.ai/user/threelevelchord)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robot operators use this skill to inspect ROS maps, maintain named waypoints, query AMCL pose, and command a ROS Noetic robot to one or more saved destinations through rosbridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Navigation commands can move a real ROS-connected robot without enough built-in safety controls or operator warnings.

Mitigation: Test in simulation or a controlled empty area, verify the map and localization, keep an emergency stop available, and supervise motion.

Risk: Imported or stale waypoint data can direct the robot toward unsafe or unreachable locations.

Mitigation: Back up waypoints before importing replacements and validate targets against the current map and costmap before navigation.

## Reference(s):

- [ROS Noetic Navigation skill page](https://clawhub.ai/threelevelchord/skills/ros-noetic-nav)
- [Publisher profile](https://clawhub.ai/user/threelevelchord)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python scripts, JSON waypoint configuration, and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ROS map summaries, waypoint records, robot pose readings, navigation status text, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
