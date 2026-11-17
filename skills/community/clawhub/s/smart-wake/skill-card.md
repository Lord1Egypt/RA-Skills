## Description:

Prevent subagent timeout using checkpoint + cron wake + resume via session spawn mechanism.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cong91](https://clawhub.ai/user/cong91)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to keep long-running or paused tasks moving by checkpointing progress, scheduling wake events, and resuming from the latest saved state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled cross-session resumes can continue work after the original session times out without enough user visibility or control.

Mitigation: Require visible pending jobs, explicit expiration, cancellation, retry limits, and clear wake reasons before enabling scheduled resumes.

Risk: Persisted checkpoints may expose more task context or artifacts than needed for resumption.

Mitigation: Store only minimal checkpoint fields needed to resume, and verify artifacts by checksum or timestamp before reuse.

Risk: Wake loops can repeatedly spawn sessions if completion or failure states are not handled.

Mitigation: Cap retry_count, mark terminal states clearly, and cancel remaining cron wakeups when the task is done or failed.

## Reference(s):

- [Smart Wake ClawHub listing](https://clawhub.ai/cong91/skills/smart-wake)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, json]

**Output Format:** [Markdown guidance with JSON checkpoint and resume packet examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should keep checkpoint contents minimal, auditable, and tied to retry and cancellation controls.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
