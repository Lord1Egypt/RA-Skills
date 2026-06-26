## Description: <br>
SQL-Linker helps agents query, insert, update, and delete records in configured MySQL, PostgreSQL, or SQLite databases with access controls and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs controlled CRUD access to known database tables, audit-log review, or bootstrap and inspection of the sql-linker configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database writes can alter or delete production records. <br>
Mitigation: Keep read_only enabled during setup and testing, and require explicit operator confirmation before running UPDATE or DELETE operations. <br>
Risk: Credential persistence and auto-resolution can expose database access if configuration or environment variables are mishandled. <br>
Mitigation: Review the generated .sql_linker configuration, keep dbpw_key secret, enable require_explicit_credential_approval for password_env or password_dpapi flows, and run set_env scripts only when persistent credential storage is acceptable. <br>
Risk: Audit logs store operator metadata and masked SQL in the target database and are not tamper-evident by themselves. <br>
Mitigation: Treat sql_audit_log as sensitive, avoid passing sensitive personal data in query parameters, and add database-layer immutable logging controls when tamper evidence is required. <br>
Risk: Bootstrap can persist configuration and password setup scripts under .sql_linker. <br>
Mitigation: Use dry-run first and run bootstrap with explicit confirmation only in the intended workspace. <br>


## Reference(s): <br>
- [SQL-Linker ClawHub release](https://clawhub.ai/cloudcode-hans/skills/sql-linker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell command snippets, configuration guidance, and database operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or inspect .sql_linker configuration files and may execute database operations when explicitly invoked.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
