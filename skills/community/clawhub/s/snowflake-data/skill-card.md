## Description:

Execute SQL queries, inspect Snowflake databases, schemas, tables, views, warehouses, and data pipeline resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and analysts use this skill to inspect Snowflake resources, run SQL queries, and manage warehouses or related data workflows through ClawLink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party ClawLink plugin handles Snowflake credentials and database actions.

Mitigation: Install only from trusted ClawHub and ClawLink sources, verify the connection path, and revoke the ClawLink connection when it is no longer needed.

Risk: The connected Snowflake role may permit broad reads or writes.

Mitigation: Use a dedicated least-privilege Snowflake role, and avoid ACCOUNTADMIN or broad write privileges.

Risk: Raw SQL, DDL, and DML can expose, modify, or delete data.

Mitigation: Review SQL before approval, require explicit confirmation for write or DDL/DML actions, and use LIMIT clauses for SELECT queries.

## Reference(s):

- [ClawHub Snowflake Skill](https://clawhub.ai/hith3sh/skills/snowflake-data)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=snowflake-data)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [Snowflake Documentation](https://docs.snowflake.com/en/)
- [Snowflake SQL Reference](https://docs.snowflake.com/en/sql-reference)
- [Snowflake REST API](https://docs.snowflake.com/en/developer-guide/sql-api/index)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and SQL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ClawLink Snowflake connection; write operations and DDL/DML queries require explicit user confirmation.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
