## Description:

An OpenClaw execution-safety policy skill that classifies action risk, limits blast radius, applies least privilege and isolation, requires dry-runs, backups, rollback planning, and verifies agent actions before completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a safety gate for OpenClaw actions that could affect files, services, production systems, databases, permissions, or secrets. It guides agents to assess risk, obtain authorization, isolate execution, verify outcomes, and recover or roll back safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The safety policy may slow or block risky actions through dry-runs, confirmations, audits, checkpoints, and recovery checks.

Mitigation: Use it where deliberate pre-flight review is acceptable, and document authorized scopes so the agent can distinguish low-risk work from actions needing stricter gates.

Risk: Trace or evaluation integrations could record sensitive operational details if configured carelessly.

Mitigation: Keep observability and evaluation integrations local or trusted, and configure them not to record secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/sandbox-blast-radius-control-engine)
- [Publisher profile](https://clawhub.ai/user/pmuhammadagus-byte)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with risk classifications, checklists, decision tables, and command recommendations when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes pre-flight review, explicit authorization, dry-run previews, local or trusted tracing, rollback plans, and post-action verification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
