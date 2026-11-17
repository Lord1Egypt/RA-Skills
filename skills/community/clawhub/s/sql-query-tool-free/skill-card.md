## Description: <br>
SQL查询工具(免费版) helps independent developers, operators, and AI agents use command-line database clients for SQL querying, parameterized execution, execution-plan analysis, CSV import/export, and cross-database syntax comparison across SQLite, PostgreSQL, MySQL, and SQL Server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to draft and execute SQL workflows through command-line database clients, including connection setup, parameterized queries, execution-plan review, data import/export, and syntax portability checks. It is not presented as a database architecture decision tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward broad database read, write, import, export, reset, and delete operations. <br>
Mitigation: Require explicit human approval before UPDATE, DELETE, INSERT, reset, import, export, production connection, or credential-backed operations. <br>
Risk: Database operations may affect sensitive or production data when run with privileged credentials. <br>
Mitigation: Prefer read-only or least-privilege database accounts, separate production credentials, and review target connection details before execution. <br>
Risk: Generated SQL or tuning guidance can be incorrect for a specific schema, engine version, or workload. <br>
Mitigation: Review proposed SQL and execution plans before running them, and test changes in a non-production environment when possible. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline SQL, Python, shell command examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include proposed database commands and structured execution results with status, data, logs, and errors.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
