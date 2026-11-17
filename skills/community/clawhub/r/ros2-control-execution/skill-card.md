## Description:

Execute ROS 2 Control state-changing commands (load, switch, unload) in a sandboxed environment. Supports parameter profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigrobinson](https://clawhub.ai/user/bigrobinson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to configure and execute allowed ROS 2 Control controller-management operations such as load, switch, unload, and state changes through a wrapper script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a command-execution weakness in a high-impact robotics context.

Mitigation: Review before installing, use only in a trusted ROS workspace, inspect config/config.json before each use, and do not run with elevated privileges.

Risk: The skill performs state-changing ROS 2 Control operations that can affect controllers and hardware behavior.

Mitigation: Do not run against real hardware until setup path handling is fixed and operational safeguards such as confirmation or dry-run are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bigrobinson/skills/ros2-control-execution)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for a ROS 2 workspace and may direct use of local configuration files.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
