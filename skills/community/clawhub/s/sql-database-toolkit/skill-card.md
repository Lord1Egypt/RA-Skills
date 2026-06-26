## Description: <br>
All-in-one SQL data analysis toolkit supporting database and file connection, SQL querying, visualization, statistical insights, and report or dashboard generation with templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqlskills](https://clawhub.ai/user/sqlskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data engineers use this skill to connect to SQL databases or local data files, run and optimize queries, create charts, and generate HTML reports or dashboards. It is suited for data exploration and reporting workflows where generated SQL and exports are reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad database, file, and report-generation authority with weak guardrails. <br>
Mitigation: Use read-only database accounts where possible, review generated SQL before execution, and avoid running against production databases without approval. <br>
Risk: Generated reports, HTML, JSON, and temporary database files may contain sensitive customer, patient, personnel, or business data. <br>
Mitigation: Export only authorized data, store generated artifacts in approved locations, and apply the same retention and access controls used for the source data. <br>
Risk: Some shell and query-termination examples are unsafe or misleading. <br>
Mitigation: Treat examples as illustrative, adapt commands and SQL to the local environment, and require review before copying them into operational workflows. <br>
Risk: Calendar heatmap output is flagged as unreliable by the security guidance. <br>
Mitigation: Avoid relying on calendar heatmap results until the implementation is fixed and validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sqlskills/sql-database-toolkit) <br>
- [Dependency installation and configuration guide](references/INSTALLATION.md) <br>
- [Integration guide](references/INTEGRATION_GUIDE.md) <br>
- [SQL security guidance](references/sql-security.md) <br>
- [SQL generation guide](references/sql-generation.md) <br>
- [Query optimization guide](references/query-optimization.md) <br>
- [Chart selection guide](references/chart-selection.md) <br>
- [Visualization guide](references/visualization-guide.md) <br>
- [Dashboard guide](references/dashboard.md) <br>
- [Template index](references/templates-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, HTML reports, charts] <br>
**Output Format:** [Markdown guidance with SQL and Python code blocks, shell commands, chart data, and generated HTML/JSON report artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create database query results, chart images or HTML, temporary database files, and report exports that can contain sensitive source data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
