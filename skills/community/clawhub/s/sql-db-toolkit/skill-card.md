## Description: <br>
Comprehensive SQL database toolkit for querying, schema inspection, data export, and migration management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to run SQL queries, inspect schemas, export data, and create backups for SQLite, PostgreSQL, and MySQL databases they specify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run write, migration, restore, or backup operations against databases the user provides. <br>
Mitigation: Use read-only or least-privilege credentials where possible and review every write, migration, restore, and backup command before execution. <br>
Risk: Connection strings may contain passwords and can appear in transcripts, logs, or schema output. <br>
Mitigation: Avoid password-bearing connection strings in shared conversations or logs and prefer secret handling outside the prompt when available. <br>
Risk: Exports and backups can contain sensitive database contents. <br>
Mitigation: Write exports and backups only to approved locations and keep them out of shared folders and source control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/sql-db-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline SQL, shell commands, and formatted query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce database exports or backups when invoked through the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
