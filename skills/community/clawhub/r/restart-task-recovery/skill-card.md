## Description:

Preserve and resume in-progress multi-agent work across OpenClaw config patch/apply restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftking100](https://clawhub.ai/user/swiftking100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to checkpoint active OpenClaw sessions before gateway restarts, generate structured resume actions after restart, and hold risky resume messages for manual confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved task text can become automatic resume messages sent to other sessions.

Mitigation: Inspect generated recovery plans before sending them and avoid automatic sessions_send for free-form recovered messages.

Risk: Checkpoint and temporary recovery files may contain sensitive task context.

Mitigation: Store checkpoint and temporary files in private locations with restrictive permissions.

Risk: Recovered messages that retry, write, create, update, delete, payment, or transfer actions may be non-idempotent.

Mitigation: Use the verifier and execution-plan flow to hold high-risk actions for explicit manual confirmation before sending.

## Reference(s):

- [Templates](references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/swiftking100/skills/restart-task-recovery)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash examples and JSON recovery payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces checkpoint files and recovery execution plans; held high-risk actions require manual confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
