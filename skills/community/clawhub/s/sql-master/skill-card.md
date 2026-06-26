## Description: <br>
SQL Master helps agents generate and optimize SQL, analyze execution plans, design indexes and warehouse schemas, access file or database data, and prepare query results for visualization across common SQL dialects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqlskills](https://clawhub.ai/user/sqlskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, analysts, and DBAs use this skill to draft production-grade SQL, diagnose slow queries, review execution plans, design indexes and schemas, and move query results into visualization or reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access local datasets, database connections, and database credentials through agent-assisted Python workflows. <br>
Mitigation: Use read-only database accounts by default, limit file access to trusted datasets, and review credentials and connection settings before use. <br>
Risk: Generated SQL, data exports, or pipeline operations could be incorrect, destructive, or written to unsafe locations if accepted without review. <br>
Mitigation: Review every SQL statement before execution, run EXPLAIN or equivalent checks for complex queries, and send exports only to known safe paths. <br>
Risk: Loading untrusted serialized or local data files can expose the environment to unsafe content. <br>
Mitigation: Avoid loading pickle files or other trusted-only formats unless the source is fully verified. <br>


## Reference(s): <br>
- [SQL Generation](references/sql-generation.md) <br>
- [Query Optimization](references/query-optimization.md) <br>
- [Index Design](references/index-design.md) <br>
- [Data Warehouse](references/data-warehouse.md) <br>
- [Hive Skew Advanced](references/hive-skew-advanced.md) <br>
- [SQL Internals](references/sql-internals.md) <br>
- [Dialect Guide](references/dialect-guide.md) <br>
- [DDL Design](references/ddl-design.md) <br>
- [SQL Security](references/sql-security.md) <br>
- [CLI Quick Reference](references/cli-quickref.md) <br>
- [Visualization Guide](references/visualization-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with SQL, Python, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL proposals, optimization reports, execution-plan guidance, data pipeline snippets, and file or database handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
