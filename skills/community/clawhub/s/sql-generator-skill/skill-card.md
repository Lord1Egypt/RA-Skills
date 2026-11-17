## Description:

Generates formatted SQL SELECT queries with Chinese comments from a natural-language request and table-structure metadata fetched for the quoted product name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengnian2013](https://clawhub.ai/user/fengnian2013)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to convert Chinese natural-language database questions into read-only SQL queries when table metadata is available through the configured schema endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the quoted product name to fetch table-structure metadata over HTTPS from the configured schema endpoint.

Mitigation: Use only approved product identifiers and schema sources, especially when working with private or production metadata.

Risk: Generated SQL can be syntactically valid but still fail to match intent or local database constraints.

Mitigation: Review generated SELECT queries before execution and test them against an appropriate non-production dataset when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengnian2013/skills/sql-generator-skill)
- [Schema endpoint base URL](https://open268v.cheyipai.com/img/c)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or plain text containing SQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SELECT-only SQL with formatting and Chinese comments; it may also return an error message when no quoted product name is found.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact manifest lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
