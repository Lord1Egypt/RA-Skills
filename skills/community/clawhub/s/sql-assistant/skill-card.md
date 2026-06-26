## Description: <br>
Use this skill when writing, reviewing, optimizing, or debugging SQL queries across PostgreSQL, MySQL, SQLite, and SQL Server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldath](https://clawhub.ai/user/goldath) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to construct SQL, diagnose slow queries, choose indexing strategies, interpret execution plans, and avoid common query anti-patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries or diagnostic examples may expose production credentials, full connection strings, customer data, or sensitive schema details if the user provides them. <br>
Mitigation: Use sanitized schema, anonymized samples, and redacted connection details when asking the agent for SQL help. <br>
Risk: Suggested indexes, triggers, transactions, or database configuration changes may affect correctness or performance in production. <br>
Mitigation: Review recommendations with a database owner and test changes in staging before applying them to production systems. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/goldath/sql-assistant) <br>
- [SQL 数据库特性对比与最佳实践](references/database-features.md) <br>
- [SQL 性能调优完整指南](references/query-optimization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL examples, review notes, and optional shell commands for database diagnostics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces advisory output only; users should test generated SQL, index changes, triggers, transactions, and configuration changes before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
