## Description: <br>
Execute SQL queries, inspect Snowflake databases, schemas, tables, views, warehouses, and data pipeline resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and data engineers use this skill to explore Snowflake resources, run SQL queries, inspect database objects, and manage warehouses from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth and sensitive Snowflake credentials through ClawLink, so an incorrect connection or excessive Snowflake grants could expose data beyond the user's intent. <br>
Mitigation: Connect only the intended Snowflake account, verify the active integration before use, and rely on Snowflake role scoping for least-privilege access. <br>
Risk: Raw SQL and DDL/DML operations can change or delete Snowflake objects when executed with sufficient privileges. <br>
Mitigation: Preview write operations, confirm the exact SQL with the user, prefer read-only inspection first, and require explicit approval before ALTER, DROP, DELETE, TRUNCATE, CREATE, or warehouse state changes. <br>
Risk: Large SELECT queries can return excessive data or increase warehouse cost. <br>
Mitigation: Use explicit LIMIT clauses for exploratory SELECT queries and confirm target database, schema, table, and warehouse before running queries. <br>
Risk: Scanner telemetry was clean, but the security evidence notes that actual skill files were not available for full verification. <br>
Mitigation: Review the published SKILL.md and installation commands before deployment, then scan the installed skill in the target environment. <br>


## Reference(s): <br>
- [Snowflake skill page](https://clawhub.ai/hith3sh/snowflake-data) <br>
- [Snowflake Documentation](https://docs.snowflake.com/en/) <br>
- [Snowflake SQL Reference](https://docs.snowflake.com/en/sql-reference) <br>
- [Snowflake REST API](https://docs.snowflake.com/en/developer-guide/sql-api/index) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL examples, connection guidance, and preview/confirmation steps for write operations.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
