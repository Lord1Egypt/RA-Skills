## Description:

Simplify SQL querying and troubleshooting for MySQL, PostgreSQL, and SQLite by helping inspect schema, generate SQL from natural language, debug SQL errors, run explain plans, lint risky SQL, and validate data with read-only execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gausszhu](https://clawhub.ai/user/gausszhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and database operators use this skill to inspect database schemas, draft and troubleshoot SQL, lint and explain queries, and summarize read-only query results across MySQL, PostgreSQL, and SQLite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-bypass options can undermine the advertised read-only safety model.

Mitigation: Use read-only database credentials, keep generated SQL in dry-run until manually reviewed, and avoid --allow-write, especially with ask.

Risk: Schema names and natural-language questions may be sent to the configured LLM service.

Mitigation: Avoid sensitive schema or business data in prompts and configure only trusted, encrypted LLM endpoints; do not set OPENAI_BASE_URL to an untrusted or plaintext service.

## Reference(s):

- [Query Patterns](references/query_patterns.md)
- [Chanquant Templates](references/chanquant_templates.md)
- [SQL Guard Copilot on ClawHub](https://clawhub.ai/gausszhu/skills/sql-guard-copilot-zhu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with SQL and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include table, JSON, or CSV shaped query output summaries when database commands are run.]

## Skill Version(s):

0.2.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
