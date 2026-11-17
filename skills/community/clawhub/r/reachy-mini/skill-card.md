## Description:

Control a Reachy Mini robot by Pollen Robotics and Hugging Face through REST API and SSH commands for movement, recorded behaviors, camera snapshots, audio direction sensing, app management, and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afalk42](https://clawhub.ai/user/afalk42)

### License/Terms of Use:


## Use Case:

Developers and robot operators use this skill to inspect and control a specific Reachy Mini robot from an agent session. It supports supervised physical movement, expressive reactions, camera capture, microphone direction-of-arrival checks, app management, and direct API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control physical movement and expressive behaviors on a real Reachy Mini robot.

Mitigation: Use it only with a supervised, intended robot and require explicit approval for movement, wake, sleep, dance, app, raw API, and system operations.

Risk: Camera snapshots and microphone direction-of-arrival checks can collect information about nearby people or spaces.

Mitigation: Run patrol and DOA behavior only with local consent, avoid unattended use, and review image paths or captured data before sharing or retaining them.

Risk: The artifact documents default SSH credentials and disables strict host-key checking in SSH helper behavior.

Mitigation: Change factory/default credentials before use, prefer pinned SSH keys, enable host-key verification, and scope SSH access to the intended robot.

Risk: Raw API and app management commands provide broad access beyond the curated movement commands.

Mitigation: Limit raw, app install/start/stop, firmware, and system actions to explicit user-approved tasks and review generated command payloads before execution.

## Reference(s):

- [Reachy Mini REST API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/afalk42/skills/reachy-mini)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, curl examples, and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that move a physical robot, capture camera images, read microphone direction-of-arrival data, manage robot apps, or use SSH.]

## Skill Version(s):

1.1.0 (source: server release metadata, created 2026-01-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
