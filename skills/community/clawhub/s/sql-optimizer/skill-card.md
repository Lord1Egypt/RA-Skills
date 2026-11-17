## Description:

Helps write dialect-appropriate SQL from business requirements and improve existing queries with indexing and rewrite recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petehuax](https://clawhub.ai/user/petehuax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to draft SQL queries, diagnose slow queries, and assess index or query-rewrite suggestions for their database dialect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated UPDATE, DELETE, or DDL statements could modify data or disrupt production workloads.

Mitigation: Review SQL before execution; preview affected rows and use transactions, backups, and a rollback plan for writes or schema changes.

Risk: SQL may be inaccurate or inefficient without the correct schema and database dialect.

Mitigation: Provide the database dialect, table structure, and indexes; confirm assumptions and inspect the execution plan before deployment.

## Reference(s):

- [SQL Optimizer on ClawHub](https://clawhub.ai/petehuax/skills/sql-optimizer)

## Skill Output:

**Output Type(s):** [Code, Guidance]

**Output Format:** [Markdown with SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, index suggestions, and EXPLAIN-based verification steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
