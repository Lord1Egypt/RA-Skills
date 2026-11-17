## Description:

SQLite database operations. Use this skill when users need to create, read, query, or modify SQLite databases (.db files).

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, query, create, and modify SQLite database files from agent workflows. It supports common sqlite/sqlite3 patterns including table creation, reads, writes, prepared statements, migrations, and database inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-capable SQLite operations can alter or delete records, especially during migrations or UPDATE/DELETE queries.

Mitigation: Use read-only copies for inspection, review write and migration SQL before execution, and back up databases before allowing write-capable operations.

Risk: Database inspection can expose sample rows from production or sensitive databases in agent output or logs.

Mitigation: Avoid running row-preview inspection on sensitive databases unless those records are acceptable to disclose; use sanitized copies when possible.

## Reference(s):

- [SQLite Client API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples; helper scripts can emit plain text tables or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include SQLite query results, schema summaries, row counts, sample rows, migration patterns, and sqlite/sqlite3 configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
