## Description: <br>
Command-line tools for SQL Server schema creation, migrations, index management, performance diagnostics, backups, restores, and bulk data import/export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqlservr](https://clawhub.ai/user/sqlservr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and database administrators use this skill to have an agent draft SQL Server command-line workflows, schema objects, migrations, indexes, diagnostics, backups, restores, and bulk import/export guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SQL Server administration guidance may include write, migration, delete, backup, or restore commands that affect live databases. <br>
Mitigation: Review generated SQL before execution, require explicit approval for production operations, and use least-privilege database accounts. <br>
Risk: Performance diagnostic queries may expose database query text or operational metadata. <br>
Mitigation: Run diagnostics only in authorized environments and avoid sharing outputs that contain sensitive query or schema details. <br>


## Reference(s): <br>
- [SQL Server Toolkit ClawHub page](https://clawhub.ai/sqlservr/sql-server-toolkit) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Usage notes](artifact/usage.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL Server administrative commands that require human review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
