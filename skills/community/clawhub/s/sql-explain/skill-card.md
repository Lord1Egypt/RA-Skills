## Description: <br>
Analyzes and explains SQL query execution plans with optimization suggestions for PostgreSQL, MySQL, and SQLite databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to format SQL, check syntax, analyze query structure and execution plans, and draft SQL from natural language before reviewing it manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated UPDATE or DELETE SQL may be incorrect or unsafe if run without review. <br>
Mitigation: Review WHERE clauses carefully and use a transaction, backup, or non-production database before execution. <br>
Risk: Optimization guidance and execution-plan explanations may be incomplete for complex database-specific behavior. <br>
Mitigation: Validate recommendations against the target database's native EXPLAIN output and performance testing. <br>


## Reference(s): <br>
- [ClawHub sql-explain listing](https://clawhub.ai/shenghoo123-png/sql-explain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text with SQL snippets, JSON-like diagnostics, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No database execution or network access is described by the server security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
