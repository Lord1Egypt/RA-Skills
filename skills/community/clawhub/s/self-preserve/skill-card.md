## Description:

Self Preserve assesses OpenClaw backup readiness and disaster recovery coverage, reports whether critical agent state has local and offsite protection, and can help manage user-confirmed backup schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinlinasd](https://clawhub.ai/user/gavinlinasd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to audit whether agent state, backups, and backup automation are sufficient for recovery after accidental edits or device-level failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses a mutable @latest installer command.

Mitigation: Verify or pin the ClawHub installer before installation.

Risk: Persistent backup scheduling creates recurring backup jobs.

Mitigation: Enable persistent scheduling only after explicit user confirmation, and review backup-related cron entries when schedules change.

Risk: Offsite backup status is declarative and cannot verify remote storage directly.

Mitigation: Treat offsite coverage as user-confirmed status and periodically test the chosen offsite copy and restore process.

## Reference(s):

- [Self Preserve on ClawHub](https://clawhub.ai/gavinlinasd/skills/self-preserve)
- [OpenClaw Agent State Model](https://docs.openclaw.dev/concepts/agent-state)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown readiness report with concise recommendations and optional backup-schedule confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only assessment by default; cron schedule changes require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
