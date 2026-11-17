## Description:

Controls and monitors ROS 2 robots through a structured rclpy CLI for topics, services, actions, parameters, lifecycle nodes, controllers, diagnostics, bags, components, and launch or run workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adityakamath](https://clawhub.ai/user/adityakamath)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to let agents inspect, operate, and troubleshoot live ROS 2 robot systems through JSON-producing CLI commands. It supports discovery, motion-related publishing, service and action calls, parameter changes, lifecycle and controller operations, diagnostics, bag inspection, and package or launch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move physical robots, change controller state, and start background sessions.

Mitigation: Install only in a controlled ROS 2 environment where operators can physically stop the robot and understand the authority granted to the agent.

Risk: The skill includes file-transfer behavior that may send local files externally through Discord uploads.

Mitigation: Use Discord upload features only where external file transfer is approved, and keep bot credentials locked down.

Risk: The security evidence reports broad autonomous robot and file-transfer authority with unsafe command and file handling.

Mitigation: Review and scan the skill before deployment, restrict runtime permissions, and operate it only in trusted robotics environments.

## Reference(s):

- [ClawHub ROS 2 Skill](https://clawhub.ai/adityakamath/skills/ros2-skill)
- [README](README.md)
- [Rules](references/RULES.md)
- [Commands](references/COMMANDS.md)
- [Examples](references/EXAMPLES.md)
- [CLI Reference](references/CLI.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command results with concise Markdown or text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require python3, ros2, rclpy, and a sourced ROS 2 environment.]

## Skill Version(s):

1.0.6 (source: server release evidence and changelog; artifact frontmatter lists 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
