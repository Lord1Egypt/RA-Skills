## Description: <br>
Analyzes SQL queries and EXPLAIN output to identify performance bottlenecks and provide optimization guidance for Databricks SQL, PostgreSQL, Spark SQL, and ANSI SQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nerikko](https://clawhub.ai/user/Nerikko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to analyze slow SQL queries or pasted query plans, understand the likely cause of bottlenecks, and receive concrete rewrite, indexing, partitioning, or database maintenance suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied SQL queries or EXPLAIN output may contain credentials, customer data, or sensitive literal values. <br>
Mitigation: Redact secrets, identifiers, and sensitive values before providing SQL or plan output to the skill. <br>
Risk: Suggested indexes, rewrites, VACUUM/ANALYZE, partitioning, or OPTIMIZE changes may have unintended effects in production. <br>
Mitigation: Test recommendations in staging, measure query plans and performance, and apply changes through normal database review and rollout processes. <br>
Risk: Dialect-specific recommendations may not fit a particular schema, data distribution, workload, or database version. <br>
Mitigation: Validate recommendations against the target database documentation and the team's knowledge of local data and workload behavior. <br>


## Reference(s): <br>
- [SQL Profiler ClawHub release](https://clawhub.ai/Nerikko/sql-profiler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with plain-English analysis, SQL examples, and optimization recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include qualitative performance estimates; does not execute SQL or connect to databases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
