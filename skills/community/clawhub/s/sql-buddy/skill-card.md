## Description:

Convert natural language to SQL, explore database schemas, execute queries safely, and get optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to turn Chinese or English natural-language questions into SQL, inspect database schemas, run or review queries, and receive optimization guidance across SQLite, PostgreSQL, MySQL, and SQL Server workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database credentials, schema details, query text, and some result values may be exposed during use.

Mitigation: Use test or database-side read-only accounts, avoid production credentials, avoid saving passwords through the skill, and limit use to data that can be shared with the configured model provider.

Risk: Advertised read-only and parameterized-query protections should not be treated as sufficient controls.

Mitigation: Review and fix the protections before relying on them, and enforce least-privilege read-only permissions at the database account level.

Risk: Generated SQL, EXPLAIN analysis, index suggestions, and result insights may be incorrect or incomplete.

Mitigation: Review generated SQL and recommendations before execution, test against non-production data first, and require explicit approval for write-capable use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/sql-buddy)
- [sql-buddy References](references/README.md)
- [Example Queries](references/example-queries.json)
- [Sample Schema](references/sample-schema.sql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON with generated SQL, dialect, execution status, result rows, schema details, EXPLAIN summaries, index suggestions, optimized SQL, insight text, and errors; result displays may also be table, JSON, CSV, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input query length is 2-2000 characters; result previews default to 20 rows.]

## Skill Version(s):

1.0.0 (source: evidence release, skill manifest, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
