## Description: <br>
Converts user-provided database schemas and plain-language data requests into syntactically correct SQL queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and non-technical users can use this skill to draft SQL from a supplied schema and a natural-language question. It is most useful when the user wants a query, an explained query, or alternative query strategies without executing anything against a database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL can be incorrect, inefficient, or unsafe to run against sensitive or production databases. <br>
Mitigation: Review each query against the intended schema, SQL dialect, permissions, and data-sensitivity requirements before execution. <br>
Risk: Missing or ambiguous schema details can lead to queries that reference the wrong tables, columns, or relationships. <br>
Mitigation: Provide explicit table names, column names, key relationships, and target SQL dialect; ask for clarification before relying on generated SQL. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with SQL code blocks and brief plain-language explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not execute SQL; asks for schema details when required tables, columns, or relationships are missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
