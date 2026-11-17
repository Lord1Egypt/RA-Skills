## Description:

Postgres best practices maintained by Supabase for Postgres running anywhere, covering schema design, SQL authoring, migrations, RLS, indexing, connection management, query performance, locking, monitoring, and advanced database features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when designing or changing Postgres databases, writing SQL, reviewing migrations, implementing RLS policies, diagnosing performance issues, and applying Supabase/Postgres best practices. It helps agents produce guidance, SQL examples, configuration suggestions, and review checklists that should be validated before production use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated guidance may include high-impact database operations such as ALTER SYSTEM, COPY, EXPLAIN ANALYZE, DROP, grants, revokes, RLS policy changes, or statistics resets.

Mitigation: Review generated SQL before execution and prefer staging environments, backups, or migration review for high-impact changes.

Risk: The skill is a documentation/reference aid, so blindly applying examples to production can introduce incorrect schema, security, or performance changes.

Mitigation: Treat outputs as proposals and validate them against the target database, access model, and deployment constraints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/supabase-postgres-best-practices)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Performance Optimization Wiki](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Supabase Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [Rule Categories](references/_sections.md)
- [Missing Indexes](references/query-missing-indexes.md)
- [Connection Pooling](references/conn-pooling.md)
- [RLS Basics](references/security-rls-basics.md)
- [Safe Constraint Migrations](references/schema-constraints.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before database changes are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
