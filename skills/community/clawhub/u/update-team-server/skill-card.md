## Description:

Update the operator-configured Team server through its canonical owner; trust native validation and acceptance without duplicate checks or schedulers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Platform operators use this skill to coordinate authorized updates of their configured Team server through its designated owner, including safe migration, recovery, and acceptance practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An interrupted live update or migration can cause service downtime or leave data stores requiring recovery.

Mitigation: Keep live execution with the designated owner and canonical controller; preserve backups and recovery records, and rely on native acceptance and recovery procedures.

## Reference(s):

- [OpenClaw database schema contracts](https://docs.openclaw.ai/reference/database-schemas)
- [OpenClaw backup semantics](https://docs.openclaw.ai/cli/backup)
- [OpenClaw Gateway restart recovery](https://docs.openclaw.ai/gateway/restart-recovery)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown guidance and concise status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No software artifacts; workflow details rely on the operator-provided private runbook and canonical updater.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
