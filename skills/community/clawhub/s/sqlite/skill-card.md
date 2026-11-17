## Description:

Use SQLite correctly with proper concurrency, pragmas, and type handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a concise SQLite reference for concurrency, pragmas, type handling, schema changes, backups, indexing, transactions, and common operational mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQLite commands or maintenance guidance can affect real database files, especially VACUUM, backups, schema migration, or transaction changes.

Mitigation: Review commands before running them, test against a copy or backup, and confirm the operation is appropriate for the target database.

Risk: SQLite concurrency, WAL, and backup behavior can cause data loss or corruption if operational details are applied incorrectly.

Mitigation: Follow the skill's guidance for WAL files, busy timeouts, transaction boundaries, and SQLite backup mechanisms before changing production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/sqlite)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline SQLite shell commands, SQL snippets, and PRAGMA examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the sqlite3 binary when command examples are used; supports linux, darwin, and win32 according to ClawHub metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
