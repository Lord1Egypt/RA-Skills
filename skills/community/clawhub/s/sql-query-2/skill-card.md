## Description:

Provides SQL guidance for query writing, performance optimization, index strategy, schema design, transaction management, and PostgreSQL-oriented operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft and review SQL queries, diagnose query performance, plan indexes, reason about schema and transaction choices, and produce database operations guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence rates the skill as suspicious because it asks for broad read, write, execution, API, and credential-related authority for SQL work.

Mitigation: Install only in environments where that authority is acceptable; restrict database, filesystem, and command permissions to the minimum needed for the task.

Risk: Generated SQL may be incorrect, destructive, or unsafe against production data.

Mitigation: Treat generated SQL as advisory, review every statement, test against non-production databases first, and use backups or transaction rollbacks for risky changes.

Risk: Generic API-key guidance could lead users to provide credentials without a clearly scoped service or purpose.

Mitigation: Do not provide API keys unless a specific trusted service and purpose are identified, and prefer short-lived or least-privilege credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/sql-query-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated SQL and database operations advice should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter reports 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
