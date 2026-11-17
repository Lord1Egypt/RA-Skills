## Description:

SQL Profiler helps data engineers and developers analyze SQL queries and EXPLAIN output to identify performance bottlenecks and produce concrete optimization guidance across Databricks SQL, PostgreSQL, Spark SQL, and ANSI SQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerikko](https://clawhub.ai/user/nerikko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and database practitioners use this skill to review slow SQL queries or query plans, understand likely causes, and get practical rewrite, indexing, partitioning, and dialect-specific tuning suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README uses an unpinned npx installer command.

Mitigation: Install from a trusted ClawHub or npm source, avoid administrator privileges, and prefer a pinned or verified installer version when available.

Risk: Queries and EXPLAIN output may contain sensitive table names, schema details, customer data, or business logic.

Mitigation: Review and redact SQL text and query plans before sharing them with an agent or external service.

Risk: Optimization suggestions may be incomplete or incorrect for a specific schema, data distribution, or runtime environment.

Mitigation: Validate changes in staging, compare real execution plans and timings, and consult database-specific documentation before applying changes in production.

## Reference(s):

- [ClawHub SQL Profiler skill page](https://clawhub.ai/nerikko/skills/sql-profiler)
- [Nerikko publisher profile](https://clawhub.ai/user/nerikko)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with SQL examples, issue summaries, explanations, and optimization recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated performance impact and dialect-specific tuning advice; recommendations should be tested against the target database and workload before use.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
