## Description: <br>
Text2sql Engine Free converts Chinese or English natural-language requests and supplied schema details into SQL for PostgreSQL, MySQL, or SQLite, with support for single-table queries, up to two-table joins, and aggregations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, data analysts, and developers use this skill to draft SQL from natural-language questions after providing database schema details. It is intended for report generation, ad hoc analysis, SQL learning, and query prototyping, not real-time stream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL or broader database actions could affect production data if executed without review, especially because requested write/exec authority is not clearly bounded. <br>
Mitigation: Use the skill as a SQL drafting helper, review every generated query manually, and run queries only with least-privilege or read-only database access unless write access is explicitly intended. <br>
Risk: Database connection handling is not fully clarified for production credentials. <br>
Mitigation: Avoid production credentials and broad database access; use scoped test credentials or managed secrets, and do not hardcode database passwords. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/text2sql-engine-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown with SQL code blocks and optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SQL should be reviewed before execution; the free edition is limited to single-table queries and up to two-table joins.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
