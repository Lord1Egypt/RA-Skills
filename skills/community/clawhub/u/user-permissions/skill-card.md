## Description:

Defines approval rules that require an agent to ask the user before system-changing or risky operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cccu-imu](https://clawhub.ai/user/cccu-imu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to require explicit user approval before agents modify configuration, services, scheduled tasks, permissions, data, networking, or runtime components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The approval thresholds may not match an operator's local policy, especially the exception for already configured scheduled tasks.

Mitigation: Review the Chinese policy text before installation and adjust local approval expectations before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cccu-imu/skills/user-permissions)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown policy guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, network behavior, persistence, or credential access was identified in the release evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
