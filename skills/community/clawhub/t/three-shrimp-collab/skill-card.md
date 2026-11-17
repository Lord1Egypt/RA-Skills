## Description:

三只虾协作系统 helps an OpenClaw multi-agent team coordinate task assignment, heartbeat checks, file monitoring, and completion notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayangai](https://clawhub.ai/user/ayangai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate a small OpenClaw assistant team with CPMO, COO, and CGO roles. It provides task queue conventions, macOS heartbeat automation, file-change monitoring, and notification templates for tracking work and reporting completed tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent background monitoring may continue watching workspace files after setup.

Mitigation: Review launchd jobs before loading them, keep only the jobs you intend to run, and unload them when monitoring is no longer needed.

Risk: Task details may be sent to hard-coded or unvalidated Feishu destinations.

Mitigation: Replace all Feishu webhook and user identifiers with approved recipients, and disable external notifications when task content is sensitive.

Risk: The artifact is tailored to a specific local account and absolute workspace paths.

Mitigation: Update hard-coded local paths and account-specific settings before installation.

Risk: Queue reset or setup commands can alter local task state.

Mitigation: Back up task queue and log files before running setup or reset commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayangai/skills/three-shrimp-collab)
- [Artifact README](artifact/README.md)
- [Skill overview](artifact/SKILL.md)
- [Automation workflow](artifact/docs/shrimp-automation-flow.md)
- [Heartbeat configuration](artifact/docs/shrimp-heartbeat-config.md)
- [Task notification specification](artifact/docs/shrimp-task-notification.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets, task queue templates, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for OpenClaw task coordination and local macOS automation setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
