## Description:

SQL Database Toolkit helps agents query SQL databases, inspect schemas, export data, analyze query plans, and create backups for SQLite, PostgreSQL, and MySQL workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query and inspect SQL databases, export results, and create backups during application development, maintenance, and data review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database queries can modify or delete data when mutating SQL is executed.

Mitigation: Use read-only or least-privilege database credentials where possible and run mutating SQL only after explicit confirmation.

Risk: Connection strings and command examples can expose database credentials.

Mitigation: Avoid placing real passwords in command lines or chats; prefer safer credential handling outside shared transcripts.

Risk: Exported CSV, JSON, SQL dump, and backup files can contain sensitive database records.

Mitigation: Treat generated exports and backups as sensitive untrusted artifacts and store, share, or delete them according to data-handling policy.

## Reference(s):

- [ClawHub SQL Database Toolkit release page](https://clawhub.ai/ericlooi504/skills/sql-db-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, SQL snippets, tabular text, JSON/CSV data, and generated export or backup files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce database exports, SQL dumps, and backup files that should be handled as sensitive artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
