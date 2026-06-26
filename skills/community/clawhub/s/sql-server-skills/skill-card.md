## Description: <br>
Comprehensive SQL Server performance diagnostics, index analysis, execution plan interpretation, query optimization, schema management, backup/restore, and monitoring using sqlcmd and T-SQL DMVs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vince-winkintel](https://clawhub.ai/user/vince-winkintel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, DBAs, and operations teams use this skill to diagnose SQL Server performance issues, analyze execution plans and indexes, guide query and schema changes, and plan backup, restore, and monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide privileged SQL Server operations such as restore, schema changes, index changes, KILL, and DBCC commands. <br>
Mitigation: Use least-privilege SQL Server accounts and require human DBA approval before any restore, schema or index change, KILL command, or DBCC command. <br>
Risk: Some guidance can affect production availability or performance, including instance-wide cache clearing and restore workflows. <br>
Mitigation: Prefer testing restores and performance fixes in non-production environments before applying them to production systems. <br>
Risk: Diagnostic output can expose operational details such as job history, errors, object names, file paths, IP addresses, or partial credentials. <br>
Mitigation: Review outputs before logging, exporting, or sharing them, and avoid storing SQL credentials or connection strings in skill files. <br>


## Reference(s): <br>
- [SQL Server skill README](artifact/README.md) <br>
- [Security considerations](artifact/SECURITY.md) <br>
- [Index strategies](artifact/sqlserver-indexes/references/index-strategies.md) <br>
- [Execution plan operators](artifact/sqlserver-execution-plans/references/plan-operators.md) <br>
- [Optimization patterns](artifact/sqlserver-query-optimization/references/optimization-patterns.md) <br>
- [Microsoft sqlcmd utility documentation](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility) <br>
- [SentryOne Plan Explorer](https://www.sentryone.com/plan-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, SQL code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline T-SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL Server diagnostic interpretations, sqlcmd invocations, generated T-SQL examples, and review-before-execution database operation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
