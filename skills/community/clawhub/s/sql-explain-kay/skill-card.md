## Description:

sql-explain helps agents and developers format SQL, check SQL syntax, analyze query structure, parse EXPLAIN output for PostgreSQL, MySQL, and SQLite, and produce optimization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database practitioners use this skill to understand SQL queries, review execution plans, generate simple SQL from natural-language requests, and identify performance concerns before changing database queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README includes a raw remote curl download path that may not match the reviewed package contents.

Mitigation: Install from the reviewed ClawHub package contents rather than an unverified raw download command.

Risk: The README includes an optional sudo system-wide symlink for the CLI entry point.

Mitigation: Avoid the system-wide symlink unless it is specifically needed, and review the target path before using sudo.

Risk: The skill can generate INSERT, UPDATE, and DELETE SQL from natural-language descriptions.

Mitigation: Review generated data-changing SQL before running it against a real database.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/sql-explain-kay)
- [ClawHub publisher profile](https://clawhub.ai/user/shenghoo123-png)
- [artifact/README.md](artifact/README.md)
- [artifact/SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, formatted SQL, JSON-style analysis objects, and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python/sqlparse-based behavior; generated SQL and optimization advice should be reviewed before database execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
