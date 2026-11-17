## Description:

Execute ROS 2 commands in a sandboxed, allowlisted environment with support for parameter profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigrobinson](https://clawhub.ai/user/bigrobinson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to configure a ROS 2 environment and execute allowlisted run, launch, service-call, and action-goal commands through the provided wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper has validation and command-execution weaknesses and should not be treated as a strong sandbox.

Mitigation: Use only in an isolated ROS environment until setup-path quoting, workspace containment checks, service/action disclosure, and argument passthrough are reviewed and fixed.

Risk: Unreviewed package allowlists or parameter profiles could permit unintended ROS command execution.

Mitigation: Keep package allowlists explicit and review parameter profiles or params files before execution; avoid secrets in profiles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigrobinson/skills/ros2-execution)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured local ROS 2 environment, explicit package allowlists, and reviewed parameter profiles or params files.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
