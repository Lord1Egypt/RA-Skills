## Description:

Comprehensive SQL Server performance diagnostics, index analysis, execution plan interpretation, query optimization, schema management, backup/restore, and monitoring using sqlcmd and T-SQL DMVs. Use when analyzing slow queries, investigating wait stats, finding missing indexes, reading execution plans, optimizing stored procedures or views, managing migrations, monitoring SQL Agent jobs, or diagnosing blocking/deadlocks on Microsoft SQL Server. Triggers on: SQL Server, MSSQL, sqlcmd, T-SQL performance, slow query, execution plan, DMV, missing index, wait stats, blocking, deadlock, stored procedure optimization, view tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and engineers use this skill to investigate SQL Server performance and operational issues, interpret diagnostic results, and prepare SQL or shell workflows for review. Production changes require DBA review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful database operations can disrupt services or alter production data.

Mitigation: Use a minimally privileged diagnostic identity and have a DBA review production changes before execution.

Risk: Diagnostic reports and backups may contain sensitive information.

Mitigation: Protect reports and backups with access controls and the operator's data handling policy.

Risk: Some workflows may refer to scripts that are not present.

Mitigation: Resolve missing script references before following those workflows.

## Reference(s):

- [SQL Server Skills on ClawHub](https://clawhub.ai/vince-winkintel/skills/sql-server-skills)
- [sqlcmd utility](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility)
- [sqlcmd output options](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility#format-options)
- [SentryOne Plan Explorer](https://www.sentryone.com/plan-explorer)
- [UPDATE STATISTICS (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/statements/update-statistics-transact-sql)
- [sp_updatestats](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-updatestats-transact-sql)
- [XML invalid characters and escape rules](https://learn.microsoft.com/en-us/sql/relational-databases/xml/invalid-characters-and-escape-rules)
- [Disable foreign key constraints](https://learn.microsoft.com/en-us/sql/relational-databases/tables/disable-foreign-key-constraints-with-insert-and-update-statements)

## Skill Output:

**Output Type(s):** [Analysis, SQL code, Shell commands, Guidance]

**Output Format:** [Markdown with T-SQL and Bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides diagnostic guidance and review-only change proposals; production changes require DBA review.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
