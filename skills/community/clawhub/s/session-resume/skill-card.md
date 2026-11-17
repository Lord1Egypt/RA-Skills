## Description:

Session Resume helps OpenClaw agents recover interrupted long-running tasks by reading a local `.task-state.json` checkpoint, reporting saved progress, and waiting for user confirmation before continuing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to checkpoint multi-step agent tasks, recover saved task state after interruptions, and decide whether to continue or abandon the recovered task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local checkpoints can expose raw task context if `.task-state.json` is synced, committed, shared, or readable by unintended users.

Mitigation: Use the skill only in protected workspaces, keep `.task-state.json` out of sync and version control, and restrict local file permissions.

Risk: Saved task context may include passwords, API keys, private keys, incident details, customer data, or sensitive command output.

Mitigation: Avoid using the skill for sensitive tasks unless it is updated to redact secrets before saving checkpoints.

Risk: Stale or forged checkpoint state could cause an agent to resume from misleading progress information.

Mitigation: Validate checkpoint provenance, expire stale checkpoints, report recovered state to the user, and wait for confirmation before continuing.

## Reference(s):

- [Session Resume Skill Page](https://clawhub.ai/wavmson/skills/session-resume)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown recovery reports with JSON task-state examples and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, update, or remove a local `.task-state.json` checkpoint as part of the agent workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
