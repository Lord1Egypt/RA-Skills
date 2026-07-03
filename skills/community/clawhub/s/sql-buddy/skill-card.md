## Description: <br>
Convert natural language to SQL, explore database schemas, execute queries safely, and get optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to translate Chinese or English natural-language questions into SQL, inspect database schemas, execute or analyze queries, and receive optimization guidance across SQLite, PostgreSQL, MySQL, and SQL Server workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to user-supplied databases and may access sensitive schemas or result samples. <br>
Mitigation: Use least-privilege read-only database accounts, point the skill only at approved datasets, and limit result previews to the minimum needed for the task. <br>
Risk: Database credentials may be supplied or saved for convenience. <br>
Mitigation: Prefer environment variables or an external secret manager, avoid saving passwords through the skill, and rotate credentials used during testing. <br>
Risk: Write execution can modify production data when allow_write is enabled. <br>
Mitigation: Keep write execution disabled by default, review generated SQL before execution, and reserve allow_write for controlled environments or explicitly approved operations. <br>
Risk: Schema details and small row samples may be included in model prompts for SQL generation or insight generation. <br>
Mitigation: Review prompt exposure for sensitive environments, mask sensitive columns, and avoid running the skill against regulated or confidential data without an approved data-handling plan. <br>


## Reference(s): <br>
- [SQL Buddy references](artifact/references/README.md) <br>
- [Example queries](artifact/references/example-queries.json) <br>
- [Sample schema](artifact/references/sample-schema.sql) <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/sql-buddy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON fields with optional table, JSON, CSV, or Markdown result formatting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated SQL, dialect, execution status, returned rows, columns, explain plans, suggested indexes, optimized SQL, schema information, insights, timing, and errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
