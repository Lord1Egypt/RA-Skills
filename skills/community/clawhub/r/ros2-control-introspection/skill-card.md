## Description:

Execute ROS 2 Control read-only introspection commands (list, view) in a sandboxed environment. Supports parameter profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigrobinson](https://clawhub.ai/user/bigrobinson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to inspect ROS 2 Control controllers, controller types, hardware components, hardware interfaces, and controller chains through read-only commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can execute unintended local shell commands if the generated ROS setup path is tampered with or contains shell-special characters.

Mitigation: Install only when the local ROS installation and generated config/config.json are trusted; review or fix the wrapper so the setup path is strictly validated or passed as a quoted positional argument, and avoid privileged shells.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigrobinson/skills/ros2-control-introspection)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only ROS 2 Control introspection using an allowlisted wrapper]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
