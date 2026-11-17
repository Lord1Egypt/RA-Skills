## Description:

Use this skill whenever the user wants to set up, configure, or refactor TypeORM within a NestJS TypeScript project, including data sources, entities, migrations, repositories, relations, and transactional patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theanswerss](https://clawhub.ai/user/theanswerss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate TypeORM into NestJS TypeScript projects, including database configuration, entity and relation design, migrations, repository wiring, transactions, and query patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample database configuration includes a DB_PASSWORD=postgres fallback that is not suitable for production.

Mitigation: Require a strong environment-provided database password, avoid password fallbacks, and use a least-privilege database role.

Risk: Generated database configuration or migrations may alter application data behavior if applied without review.

Mitigation: Review generated TypeORM configuration and migration files before execution, and keep synchronize disabled outside local development.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript, JSON, shell, and environment configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance and code snippets for adapting NestJS TypeORM patterns to an existing project structure.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
