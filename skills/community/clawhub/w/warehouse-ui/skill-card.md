## Description: <br>
Universal database IDE CLI — query PostgreSQL, MySQL, SQLite, BigQuery, MongoDB with cost projection <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olegnazarov23](https://clawhub.ai/user/olegnazarov23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data engineers, and agents use this skill to connect to supported databases, inspect schemas, run SQL or database queries, estimate BigQuery query costs, and generate SQL from natural language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect to real databases and execute SQL, including AI-generated SQL. <br>
Mitigation: Use read-only or least-privilege database credentials, avoid privileged saved production connections, and review generated SQL before execution. <br>
Risk: Queries may expose sensitive schemas or business data to configured AI providers. <br>
Mitigation: Review AI-provider data handling before using AI-assisted queries with sensitive databases. <br>
Risk: Database queries, especially BigQuery queries, can consume resources or incur costs. <br>
Mitigation: Use dry-run and query limits where available before executing expensive or broad queries. <br>


## Reference(s): <br>
- [Warehouse UI ClawHub listing](https://clawhub.ai/olegnazarov23/warehouse-ui) <br>
- [Warehouse UI GitHub repository](https://github.com/olegnazarov23/warehouse-ui) <br>
- [Warehouse UI GitHub releases](https://github.com/olegnazarov23/warehouse-ui/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, SQL, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples; CLI commands return JSON by default] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Database query output may include columns, rows, row counts, duration, and BigQuery cost estimates.] <br>

## Skill Version(s): <br>
0.10.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
