## Description:

Generates and executes SQL queries against a retail database from natural-language requests, using the provided schema directly instead of a semantic layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyujun](https://clawhub.ai/user/jackyujun)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts and retail data users use this skill to ask natural-language questions, generate SQL for sales, inventory, customer, store, and product analyses, and execute the query through the configured Gateway JDBC interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad database query access can expose member, employee, address, order-level, or other person-level records.

Mitigation: Install only where users are authorized to query the retail database, prefer a restricted gateway role or approved analytics views, audit queries, and require redaction or approval before returning person-level records.

Risk: The artifact recommends bypassing proxies for Gateway API requests.

Mitigation: Remove the global proxy bypass and route requests through the environment's approved network controls.

Risk: Generated SQL can use an incorrect metric definition because the skill directly maps natural language to schema fields without a semantic layer.

Mitigation: Require users or reviewers to confirm ambiguous metric definitions, especially for sales amount, average order value, discount, return rate, and other derived metrics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackyujun/skills/text-to-sql-query)
- [Gateway JDBC SQL query endpoint](https://gateway.can.aloudata.com/api/jdbc/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with SQL, curl, and Python code blocks; query results are returned as Markdown tables or plain-text errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAN_API_KEY and access to the configured Gateway JDBC endpoint; queries are intended to be SELECT-only against the documented whitelist tables.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
