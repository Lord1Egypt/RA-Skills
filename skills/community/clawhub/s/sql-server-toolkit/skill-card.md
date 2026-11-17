## Description:

Command-line toolkit for Microsoft SQL Server schema creation, migrations, index management, performance diagnostics, backups, restores, and bulk data import/export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sqlservr](https://clawhub.ai/user/sqlservr)

### License/Terms of Use:


## Use Case:

Developers and database engineers use this skill to draft and run SQL Server command-line workflows for schema setup, migrations, indexing, backup and restore operations, bulk import/export, and performance diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default connection examples can encourage use of SQL Server administrator credentials or exposed passwords.

Mitigation: Prefer integrated authentication or interactive password prompts, and avoid the sa account for routine work.

Risk: The backup example uses FORMAT and INIT, which can overwrite or reinitialize an existing backup file.

Mitigation: Run backup commands only when the target file and recovery plan are intentional, and keep independent recovery copies.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline sqlcmd, bcp, and SQL code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable SQL and command-line examples that should be reviewed before use in a production database.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
