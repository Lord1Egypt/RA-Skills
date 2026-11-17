## Description:

Analyze and explain SQL execution plans, format SQL, check syntax, summarize SQL structure, and generate simple SQL from natural-language requests for PostgreSQL, MySQL, and SQLite workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to inspect SQL plans, identify common query-performance issues, format or check SQL, and draft simple SQL statements from business-language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README includes unsafe installation guidance that can lead users to download and run unverified code.

Mitigation: Use bundled local files or a verified release, and avoid curl-based installation unless the source is pinned and checksum-verified.

Risk: The README suggests optional system-wide command installation with sudo.

Mitigation: Avoid sudo unless a system-wide command is intentionally required; prefer a user-local path or direct script execution.

Risk: Generated UPDATE or DELETE SQL may modify data if executed without review.

Mitigation: Treat generated SQL as a draft and review it carefully before running it against a real database.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/sql-explain)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, SQL snippets, JSON-style analysis results, plain text, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local and rule-based; generated SQL should be reviewed before use against production data.]

## Skill Version(s):

1.0.0 (source: release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
