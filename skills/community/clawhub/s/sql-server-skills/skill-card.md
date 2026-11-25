## Description:

A reference skill for diagnosing, tuning, and managing SQL Server with sqlcmd and T-SQL DMVs, covering performance, indexes, execution plans, schemas, backups, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and engineers use this skill to investigate SQL Server performance and operational issues, interpret query plans, and prepare SQL or sqlcmd guidance for database changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some suggested query rewrites may change query results.

Mitigation: Review each rewrite against the intended semantics and validate it with representative data before use.

Risk: The security scan had partial coverage because many referenced local files were missing from the scanned artifact.

Mitigation: Review the referenced files before relying on guidance that depends on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/vince-winkintel/skills/sql-server-skills)
- [Microsoft sqlcmd utility documentation](https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility)
- [Microsoft UPDATE STATISTICS documentation](https://learn.microsoft.com/en-us/sql/t-sql/statements/update-statistics-transact-sql)
- [Microsoft guidance on disabling foreign key constraints](https://learn.microsoft.com/en-us/sql/relational-databases/tables/disable-foreign-key-constraints-with-insert-and-update-statements)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline T-SQL and Bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic queries and operational examples; proposed database changes require review appropriate to the target.]

## Skill Version(s):

1.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
