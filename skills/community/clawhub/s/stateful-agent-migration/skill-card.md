## Description:

Migrate or upgrade heavy stateful OpenClaw agents with rehearsal, embedding safety, rollback, and live proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[posthuman](https://clawhub.ai/user/posthuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to rehearse, migrate, validate, and if needed roll back stateful OpenClaw deployments while preserving service ownership, credentials, and agent state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Concurrent Gateway, automation, or supervisor writes during migration can leave state inconsistent or trigger an unintended restart.

Mitigation: Inventory writers, pause and fence them for cutover, rehearse against an isolated copy, and require verified recovery points and live acceptance checks.

Risk: Backups and migration artifacts may contain credentials or user content.

Mitigation: Protect backups like live state and keep reports redacted; exclude credentials, raw configuration, transcripts, messages, and database rows.

Risk: Migration or repair commands can change production state or cause external side effects.

Mitigation: Use an authorized maintenance window, block outbound delivery and service-manager actions during rehearsal, and verify rollback before production cutover.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/posthuman/skills/stateful-agent-migration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown runbook with checklists, shell commands, and reporting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operational steps and acceptance gates are tailored to the deployment's versions, services, state, and integrations.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
