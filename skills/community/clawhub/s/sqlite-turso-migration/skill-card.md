## Description: <br>
Provides a Prisma PostgreSQL to SQLite/Turso migration pattern for converting production Postgres schemas to edge-compatible SQLite with optional Turso replication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan migrations from Prisma-managed PostgreSQL databases to local SQLite or edge-replicated Turso setups. It focuses on schema type mapping, migration flow, validation, rollback planning, and lower-cost or local-first database operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration commands or generated scripts could change production data incorrectly. <br>
Mitigation: Run against backups or staging copies first, review proposed commands and scripts before execution, and verify migrated data before switching traffic. <br>
Risk: Database credentials may grant broader access than the migration requires. <br>
Mitigation: Use scoped credentials and avoid granting production access beyond the migration task. <br>
Risk: PostgreSQL features such as arrays, enums, UUIDs, and auto-increment behavior may not map exactly to SQLite or Turso. <br>
Mitigation: Review type mappings, generated schema changes, and validation results before accepting the migrated schema. <br>


## Reference(s): <br>
- [Skill definition](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/nissan/sqlite-turso-migration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference database connection environment variables and migration commands that should be reviewed before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
