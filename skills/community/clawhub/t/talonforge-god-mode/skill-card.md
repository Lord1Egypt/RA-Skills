## Description:

Enables OpenClaw agents to autonomously execute prioritized tasks on a heartbeat loop with logging, auditing, error handling, and workspace hygiene.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperzinou](https://clawhub.ai/user/casperzinou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run an agent from a prioritized task queue on scheduled heartbeats, with state tracking, audit logs, and guardrails for autonomous cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous heartbeat cycles may execute broad tasks with limited human control.

Mitigation: Run the skill only in a dedicated workspace with limited tools and file permissions, and require manual approval for shell, network, external API, and out-of-queue tasks.

Risk: Workspace hygiene behavior can move, delete, or truncate files if scoped too broadly.

Mitigation: Disable or narrow the hygiene sweep before use, review HEARTBEAT.md and TASKS.md, and keep backups for workspaces where deletion or truncation would be harmful.

Risk: Untrusted task queue entries can steer the agent into unsafe or unintended work.

Mitigation: Keep TASKS.md under trusted human review and require explicit approval for red-line tasks such as money, contracts, irreversible actions, file deletion, log truncation, and external side effects.

## Reference(s):

- [God Mode ClawHub listing](https://clawhub.ai/casperzinou/skills/talonforge-god-mode)
- [HEARTBEAT template](artifact/references/HEARTBEAT-template.md)
- [TASKS template](artifact/references/TASKS-template.md)
- [God Mode state template](artifact/references/god-mode-state-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or Markdown templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace TASKS.md, HEARTBEAT.md, and memory state files when the setup script is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
