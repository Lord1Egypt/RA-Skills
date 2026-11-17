## Description:

Write and execute Timeplus streaming SQL for real-time analytics, including streams, streaming queries, materialized views, ingestion, sinks, UDFs, random streams, and ClickHouse-compatible HTTP execution with Timeplus environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangtao](https://clawhub.ai/user/gangtao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, validate, and execute Timeplus streaming SQL for real-time analytics workflows, including data ingestion, transformations, alerts, tasks, sinks, UDFs, and test streams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce SQL and curl commands that operate on a real Timeplus environment, including privileged DDL and DML actions.

Mitigation: Use least-privilege Timeplus credentials and require explicit human approval before DROP, ALTER, DELETE, CREATE VIEW, CREATE ALERT, CREATE TASK, or package-install actions.

Risk: Credential handling examples may lead to plaintext secrets in URLs, shell history, logs, or SQL definitions if adapted carelessly.

Mitigation: Store credentials in environment variables or approved secret management, use HTTPS/TLS, and avoid embedding credentials in URLs or SQL definitions.

Risk: Sink, alert, webhook, Slack, S3, Kafka, or database output guidance can route sensitive data to external destinations.

Mitigation: Review every external sink or notification target before execution and confirm that destination, payload, and access controls are approved for the data being sent.

Risk: Server-side package installation or UDF guidance can expand execution risk in the Timeplus runtime.

Mitigation: Allow package installation and UDF deployment only after code review, dependency review, and confirmation that the runtime is isolated for the intended workload.

## Reference(s):

- [Timeplus documentation](https://docs.timeplus.com)
- [Timeplus Proton repository](https://github.com/timeplus-io/proton)
- [ClawHub skill page](https://clawhub.ai/gangtao/skills/timeplus-sql-guide)
- [Getting Data Into Timeplus](references/INGESTION.md)
- [Data Transformations in Timeplus](references/TRANSFORMATIONS.md)
- [Sending Data Out of Timeplus](references/SINKS.md)
- [Timeplus SQL Reference](references/SQL_REFERENCE.md)
- [Random Streams - Skill Guide for Timeplus SQL Agent](references/RANDOM_STREAMS.md)
- [User-Defined Functions in Timeplus](references/UDFS.md)
- [Timeplus Python Table Functions - Skill Guide](references/Python_TABLE_FUNCTION.md)
- [EMIT Clauses and UDAF Emit Control](references/EMIT_AND_UDAF.md)
- [Scheduled Tasks in Timeplus](references/TASK.md)
- [Real-time Alerts in Timeplus](references/ALERT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Timeplus SQL statements, curl commands, environment-variable setup, and operational guidance for real Timeplus deployments.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
