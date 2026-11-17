## Description:

Read and query SQLite database files. Use when user wants to inspect or extract data from .sqlite files, especially OpenClaw's main.sqlite memory database. Supports basic SELECT queries, table listing, and schema inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[senknight](https://clawhub.ai/user/senknight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect SQLite databases, list tables, view table schemas, run SQL queries, and export selected query results while investigating local application data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can execute arbitrary SQL against a database file and may change or damage writable databases despite the skill being presented as read-oriented.

Mitigation: Use database copies or read-only files, and allow only trusted users or reviewed instructions to provide SQL queries.

Risk: CSV export writes to a caller-provided output path, which can expose sensitive query results or overwrite an unintended file.

Mitigation: Review output paths before execution and write exports only to approved working directories.

## Reference(s):

- [SQLite Schema Reference](artifact/references/schema.md)
- [ClawHub Skill Page](https://clawhub.ai/senknight/skills/sqlite-reader)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown with inline shell and Python command examples; terminal text output or CSV export from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query execution depends on the SQLite database path, selected action, optional SQL query, optional row limit, and optional CSV output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
