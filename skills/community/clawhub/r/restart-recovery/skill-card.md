## Description:

Make OpenClaw agent workflows restart-safe using checkpoint files, idempotent step tracking, wake/resume handoff, and stale-checkpoint monitoring for recovery and progress preservation across restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanrails](https://clawhub.ai/user/stanrails)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add checkpoint, restart, wake, and resume workflows around restart-prone operations such as updates, service restarts, and long-running jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checkpoint script can write outside the intended checkpoint directory when workflow IDs are untrusted.

Mitigation: Use only trusted workflow IDs and trusted workspaces until path confinement is fixed.

Risk: Resume does not validate checkpoint schema or checkpoint hash as documented, so untrusted or corrupted checkpoints may be resumed.

Mitigation: Review checkpoint files before resume and add schema and hash validation before deploying in sensitive workflows.

Risk: Checkpoint files can expose sensitive workflow details if operators place secrets or tokens in checkpoint fields.

Mitigation: Keep secrets and tokens out of checkpoint files and review checkpoint retention and cleanup policies.

## Reference(s):

- [Checkpoint schema](references/checkpoint-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON checkpoint files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a checkpoint JSON schema, local Python helper scripts, and stale-checkpoint alert output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
