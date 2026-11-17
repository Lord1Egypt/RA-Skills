## Description:

SQL Generator helps agents draft SQL queries, explanations, optimizations, DDL, seed data, migration-oriented snippets, and quick SQL reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data practitioners, and technical teams use this skill to generate SQL examples, table definitions, indexes, mock INSERT data, and optimization guidance for common database tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL can include DDL, INSERT, index, migration, UPDATE, DELETE, DROP, or ALTER statements that may be incorrect or destructive.

Mitigation: Review every generated statement before execution, test in staging first, keep backups, use transactions where appropriate, and run with least-privileged database accounts.

Risk: The bundled sql-generator wrapper records command history locally, which may expose sensitive SQL, customer identifiers, credentials, or private file paths.

Mitigation: Avoid passing sensitive inputs to the wrapper unless local history logging is acceptable; clear local history files according to organizational policy.

Risk: Server security evidence flags mismatched scripts and unsafe SQL text generation from unvalidated names.

Mitigation: Inspect the installed scripts before use and validate table names, column names, and generated identifiers before running any output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/sql-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/ckchzh)
- [tips.md](artifact/tips.md)
- [BytesAgain homepage](https://bytesagain.com)
- [BytesAgain feedback](https://bytesagain.com/feedback)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with SQL and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated examples and recommendations that should be reviewed before use against real databases.]

## Skill Version(s):

2.3.7 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
