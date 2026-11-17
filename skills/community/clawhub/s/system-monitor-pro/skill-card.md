## Description:

Real-time OpenClaw system monitoring with formatted terminal output for CPU, memory, disk, NVIDIA GPU, Gateway, cron jobs, model quota, and multi-machine checks on macOS and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check local or SSH-accessible OpenClaw host health, review resource usage, and surface threshold-based alerts in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that optional remote SSH mode should be reviewed before installation.

Mitigation: Avoid --remote until remote command construction uses argument arrays or strict validation and host-key checking is restored.

Risk: Periodic automatic monitoring can run local system-status commands without a direct user prompt.

Mitigation: Do not add the suggested recurring HEARTBEAT entry unless periodic automatic monitoring is intended, and keep triggers narrow.

## Reference(s):

- [System Monitor Pro on ClawHub](https://clawhub.ai/dagangtj/skills/system-monitor-pro)
- [Publisher profile: dagangtj](https://clawhub.ai/user/dagangtj)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Terminal-style text status card, alert-only text summary, or formatted JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local checks by default and optional SSH remote monitoring with --remote.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
