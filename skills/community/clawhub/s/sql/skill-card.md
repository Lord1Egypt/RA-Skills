## Description: <br>
Master relational databases with SQL. Schema design, queries, performance, migrations for PostgreSQL, MySQL, SQLite, SQL Server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as SQL reference material for designing schemas, writing and optimizing queries, building migrations, and managing backups across SQLite, PostgreSQL, MySQL, and SQL Server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database examples can be dangerous if copied into production, including DROP, ALTER, RESTORE, DELETE, and session-termination commands. <br>
Mitigation: Verify the database target, confirm backups, test restores in staging or a new database, and require explicit approval before running destructive or session-termination commands. <br>
Risk: Operational examples may affect real data or availability when used against live databases. <br>
Mitigation: Review each command before execution and prefer staging, test databases, or read-only checks unless a production change has been approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/sql) <br>
- [Skill Homepage](https://clawic.com/skills/sql) <br>
- [SQL Skill Definition](artifact/SKILL.md) <br>
- [Operations Guide](artifact/operations.md) <br>
- [Query Patterns](artifact/patterns.md) <br>
- [Schema Design Patterns](artifact/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with SQL, shell, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples may require sqlite3, psql, mysql, or sqlcmd depending on the database target.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
