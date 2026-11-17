## Description:

Provides a migration pattern for moving Prisma-managed PostgreSQL schemas to SQLite or Turso, including dialect conversion guidance, Turso sync, and validation considerations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and review migrations from Prisma-managed PostgreSQL databases to local SQLite or edge-replicated Turso deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database migrations can modify, move, or expose sensitive production data.

Mitigation: Use least-privilege database credentials, take backups, test migrations on a copy first, and review generated migration scripts before using them on real data.

Risk: The skill uses outbound network access for Turso cloud schema sync and optional replication.

Mitigation: Confirm the target Turso database and use scoped credentials such as TURSO_DATABASE_URL and TURSO_AUTH_TOKEN before running sync or replication steps.

Risk: The artifact describes a draft migration guide with planned capabilities.

Mitigation: Review the proposed migration approach and validation harness before applying it to production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/sqlite-turso-migration)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with migration steps, code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference TURSO_DATABASE_URL, TURSO_AUTH_TOKEN, and DATABASE_URL environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
