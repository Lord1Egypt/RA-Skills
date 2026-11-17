## Description:

数据库模式设计 helps agents turn project requirements into production-oriented database schemas, ER diagrams, DDL, index strategies, migration plans, and design reviews for systems such as MySQL, PostgreSQL, MongoDB, Redis, and Milvus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or review database schemas from business requirements, including entity modeling, normalization, database selection, index planning, migration strategy, and security checks. It is especially relevant when an agent needs to produce ER diagrams, table structures, SQL DDL, or schema review guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DDL, migration scripts, or index changes could cause data loss, table locks, downtime, or performance regressions if applied directly to a real database.

Mitigation: Review all SQL and migration recommendations, test them in staging, maintain backups and rollback scripts, and pay special attention to ALTER, DROP, and indexing changes.

Risk: Schema recommendations may be incomplete when workload, data growth, consistency, privacy, or security requirements are underspecified.

Mitigation: Collect the required business entities, relationships, data volume, read/write patterns, consistency needs, and sensitive-field handling before adopting the design.

## Reference(s):

- [数据库模式设计 - 详细参考](artifact/references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/qqyougit-database-schema-designer)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Mermaid ER diagrams, tables, and SQL DDL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output with English DDL and field names]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter is 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
