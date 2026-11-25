## Description:

Validates migration SQL, analyzes index health, and applies pending schema migrations to the target database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate pending SQLite migration files, inspect index health, and apply schema migrations for an application database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically write cleanup migrations and drop indexes in the target database.

Mitigation: Use only on disposable or backed-up databases until cleanup generation and execution require explicit approval.

Risk: Migration validation is performed against the configured database connection.

Mitigation: Validate migrations in an isolated database before connecting the skill to production or shared data.

Risk: Generated SQL uses discovered index names in DROP INDEX statements.

Mitigation: Quote SQL identifiers safely and review generated migration files before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ink5725/skills/schema-manager)

## Skill Output:

**Output Type(s):** [JSON, code, shell commands]

**Output Format:** [JSON status output with generated SQL migration files when cleanup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write cleanup migration files and execute database changes against the configured SQLite database.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
