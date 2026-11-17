## Description:

A local SQL helper for formatting SQL, checking syntax, analyzing query structure, converting simple natural-language requests into SQL, and interpreting PostgreSQL-style EXPLAIN output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to inspect SQL, explain query plans, and draft simple SQL statements while working with PostgreSQL, MySQL-compatible, or SQLite queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions may fetch executable Python from a mutable GitHub branch without verification.

Mitigation: Review the install path before use; prefer the bundled sql_explain.py from the reviewed package, or require a pinned commit and SHA-256 verification before running downloaded code.

Risk: Generated INSERT, UPDATE, and DELETE SQL can change data if executed directly.

Mitigation: Treat generated SQL as a draft and require human review before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/sql-explain-cli)
- [sqlparse package](https://pypi.org/project/sqlparse/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text, Markdown-style reports, JSON-like diagnostics, SQL snippets, and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated INSERT, UPDATE, and DELETE SQL should be treated as drafts for human review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
