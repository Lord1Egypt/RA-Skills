## Description:

Deep SQL performance workflow for symptom framing, execution-plan analysis, indexing strategy, query rewrites, locking and transaction behavior, statistics, partitioning, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to diagnose and improve SQL performance by framing symptoms, measuring baselines, reading execution plans, tuning indexes and queries, and verifying changes on realistic data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL parameters, execution plans, and production diagnostics may contain secrets or unnecessary production values.

Mitigation: Redact secrets and minimize production-specific values before sharing SQL, parameters, plans, or logs with the agent.

Risk: Index or DDL recommendations can affect write performance, locking, storage usage, or availability if applied directly to production.

Mitigation: Test proposed changes in staging or another production-like environment, measure impact, and prepare a rollback path before production rollout.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/sql-optimization)
- [Publisher Profile](https://clawhub.ai/user/codekungfu)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with SQL, DDL, and command examples when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory optimization plans and verification checklists; does not execute database changes itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
