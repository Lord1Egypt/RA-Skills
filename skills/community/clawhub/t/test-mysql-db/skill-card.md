## Description:

Connect to test-environment MySQL databases for troubleshooting, data verification, schema inspection, and controlled validation queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraskittles](https://clawhub.ai/user/extraskittles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect test or development MySQL data, validate whether application code wrote expected records, compare before and after states, and perform explicitly approved low-risk data corrections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can modify database data when write execution is allowed.

Mitigation: Install only for disposable or well-scoped test databases and require explicit confirmation, narrow predicates, expected row counts, and rollback plans before writes.

Risk: The helper's read-only safeguard is bypassable and should not be treated as a security boundary.

Mitigation: Use least-privilege, preferably server-enforced read-only MySQL credentials for normal use.

Risk: Database credentials and query outputs may contain sensitive information.

Mitigation: Avoid command-line passwords, use TEST_MYSQL_* environment variables or scoped secret handling, and redact passwords, tokens, personal data, payment data, and secrets from final responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/extraskittles/skills/test-mysql-db)
- [Skill definition](artifact/SKILL.md)
- [MySQL query helper](artifact/scripts/mysql_query.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with SQL snippets, shell commands, and optional table, JSON, or CSV query results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redacts secrets in summaries and reports non-secret connection or validation findings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
