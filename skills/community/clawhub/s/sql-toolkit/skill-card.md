## Description:

Query, design, migrate, and optimize SQL databases for SQLite, PostgreSQL, and MySQL without relying on ORMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for direct command-line database work, including schema design, SQL query writing, migrations, indexing, backup and restore, and slow-query debugging across SQLite, PostgreSQL, and MySQL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration and restore examples can overwrite or corrupt real data if applied to the wrong database or without adequate safeguards.

Mitigation: Verify the target database and connection string, make a backup first, and avoid running restore commands against production database names.

Risk: Manual migration snippets may apply unvalidated files or leave a database in an inconsistent state if a step fails.

Mitigation: Validate migration filenames and contents before use, and prefer transactional or tool-managed migrations where available.

## Reference(s):

- [ClawHub SQL Toolkit skill page](https://clawhub.ai/gitgoodordietrying/skills/sql-toolkit)
- [ClawHub publisher profile: gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples assume the user verifies target databases, connection strings, migration files, and backup or restore destinations before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
