## Description: <br>
SQLite database operations. Use this skill when users need to create, read, query, or modify SQLite databases (.db files). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect SQLite database structure, run SQL queries, create or update tables and rows, and apply migration patterns for .db files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can display or change data in SQLite files the user points it at. <br>
Mitigation: Use copies or backups for important databases, verify the database path before commands run, and avoid querying tables that contain secrets or personal data unless that data is intended to appear in output or logs. <br>


## Reference(s): <br>
- [SQLite Client API Reference](references/api.md) <br>
- [ClawHub release page](https://clawhub.ai/openlark/sqlite-client) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript, SQL, and shell command examples; helper scripts may emit plain text tables or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can inspect database schemas, show sample rows, execute read and write SQL, and return query results from user-selected SQLite files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
