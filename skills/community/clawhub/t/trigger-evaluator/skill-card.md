## Description:

Evaluate real OpenClaw trigger rules against the current database state, especially stale mission detection backed by public.openclaw_* tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecosincronia](https://clawhub.ai/user/ecosincronia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run the implemented OpenClaw stale_missions_alert evaluator and inspect the current trigger rule row in the database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes an external local OpenClaw engine script that was not reviewed as part of the packaged artifact.

Mitigation: Install only in trusted OpenClaw workspaces and pin or package the engine script before broader use.

Risk: The inspection path uses Docker and PostgreSQL access that may be broader than the narrow trigger-read task requires.

Mitigation: Prefer a dedicated read-only database role and restrict Docker/PostgreSQL access to the minimum needed environment.

## Reference(s):

- [Trigger Evaluator on ClawHub](https://clawhub.ai/ecosincronia/skills/trigger-evaluator)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are limited to the supported stale_missions_alert trigger workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
