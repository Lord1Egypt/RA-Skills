## Description:

Use this skill to write, review, optimize, and debug SQL queries, including query construction, performance tuning, index strategy, window functions, CTEs, and common anti-patterns for PostgreSQL, MySQL, and SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldath](https://clawhub.ai/user/goldath)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to construct, review, debug, and optimize SQL queries across PostgreSQL, MySQL, and SQLite. It supports index design, EXPLAIN analysis, pagination patterns, CTEs, window functions, database feature comparison, and slow-query diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL or optimization advice may be incorrect for the target database, schema, workload, or data distribution.

Mitigation: Review generated SQL against the target environment, inspect execution plans, and test changes outside production before applying them.

Risk: Mutation, indexing, partitioning, or configuration commands can affect production data, availability, or performance if run blindly.

Mitigation: Use normal database change controls, backups, maintenance windows, and rollback plans before executing operational commands.

Risk: Slow-query logs and diagnostics may expose schema details or user-derived values.

Mitigation: Redact sensitive values and restrict access before sharing logs or query samples with an agent.

## Reference(s):

- [SQL 数据库特性对比与最佳实践](references/database-features.md)
- [SQL 性能调优完整指南](references/query-optimization.md)
- [ClawHub skill page](https://clawhub.ai/goldath/skills/sql-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, shell, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language SQL guidance; generated SQL and database operations should be reviewed for the target database and environment before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
