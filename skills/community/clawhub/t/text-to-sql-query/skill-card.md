## Description: <br>
Generates and executes SELECT-only SQL against a retail database from natural-language questions, returning the query interpretation, SQL, and results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyujun](https://clawhub.ai/user/jackyujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail analysts and business users use this skill to ask natural-language questions about sales, inventory, product launches, shops, products, and members, then receive SQL and Markdown query results from approved database tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent credentialed live access to sensitive retail and member data. <br>
Mitigation: Use a read-only, least-privilege CAN_API_KEY limited to the listed tables and review the generated SQL before execution. <br>
Risk: Queries may return member names, VIP IDs, order numbers, seller names, or other identifiers. <br>
Mitigation: Avoid returning identifiers unless explicitly authorized, and keep filters and LIMIT values tight. <br>
Risk: Ambiguous business metrics can produce incorrect SQL or misleading results. <br>
Mitigation: Confirm metric definitions when unclear, document the chosen calculation in the query interpretation, and use the provided schema and JOIN rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackyujun/text-to-sql-query) <br>
- [Gateway JDBC SQL query API](https://gateway.can.aloudata.com/api/jdbc/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with a natural-language query interpretation, SQL code block, and result table.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAN_API_KEY at runtime and returns live database query results; agents should review generated SQL before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
