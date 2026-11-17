## Description: <br>
SQL大师工具(免费版) helps independent developers, operators, and AI agents work with SQLite, PostgreSQL, and MySQL schemas, queries, indexes, migration scripts, backups, and restore workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database operators, DBAs, data analysts, and AI agents use this skill to draft and review SQL-oriented database development and operations guidance, including schema design, complex queries, indexing, migrations, backup and restore steps, and command-line database workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide command execution or write-enabled database changes against production or shared databases. <br>
Mitigation: Review the skill before installation, use explicit database targets, keep current backups, and require human confirmation for migrations, imports, restores, UPDATE/DELETE statements, and shell execution. <br>
Risk: Database guidance can be destructive or incorrect if applied to the wrong environment or without checking generated SQL. <br>
Mitigation: Inspect generated SQL and commands before running them, prefer staging environments first, and use transactions or rollback plans where supported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/sql-master-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, SQL code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with SQL, shell command, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose database write operations and command execution; outputs should be reviewed before use against production or shared databases.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
