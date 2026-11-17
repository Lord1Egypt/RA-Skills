## Description:

Warehouse UI is a universal database IDE CLI for querying PostgreSQL, MySQL, SQLite, BigQuery, and MongoDB with cost projection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olegnazarov23](https://clawhub.ai/user/olegnazarov23)

### License/Terms of Use:


## Use Case:

External developers and data teams use this skill to connect agents to databases, inspect schemas, run or dry-run queries, estimate BigQuery cost, and generate SQL from natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a native binary that evidence.security describes as unverified.

Mitigation: Review the release before installing and verify the downloaded binary where possible.

Risk: Database credentials and queried data may be sensitive.

Mitigation: Use least-privilege, preferably read-only database accounts, and avoid placing real passwords in command-line arguments or connection URLs.

Risk: AI query generation may send schema, prompts, or data context to the configured provider.

Mitigation: Do not use AI query generation with sensitive schema, prompts, or data unless that sharing is acceptable for the deployment.

## Reference(s):

- [Warehouse UI ClawHub skill page](https://clawhub.ai/olegnazarov23/skills/warehouse-ui)
- [Warehouse UI GitHub repository](https://github.com/olegnazarov23/warehouse-ui)
- [Warehouse UI GitHub releases](https://github.com/olegnazarov23/warehouse-ui/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON-oriented CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI outputs JSON to stdout by default and can produce table output when requested.]

## Skill Version(s):

0.10.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
