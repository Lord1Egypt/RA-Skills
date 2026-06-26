## Description: <br>
Use when a user provides a SQL query or result set and asks to generate a chart, dashboard, or data visualization from the results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and agent users use this skill to turn SQL queries or tabular query results into chart specifications and multi-panel dashboard drafts. It helps choose an appropriate visualization type, map columns to axes, and avoid misleading charts for empty or oversized result sets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated charts or dashboards may be misleading if the SQL result shape is inferred incorrectly, the result set is empty, or large datasets are sampled or aggregated. <br>
Mitigation: Treat generated dashboards as drafts, verify column mappings and chart type against the actual query result, and disclose any sampling or aggregation applied to large datasets. <br>
Risk: SQL query results may contain sensitive data shared with the agent environment. <br>
Mitigation: Avoid pasting sensitive query results unless sharing them with the agent environment is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangjipeng977/sql-to-dashboard) <br>
- [Skill metadata source](https://github.com/MiniMax-AI/skills) <br>
- [Reference index](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, configuration] <br>
**Output Format:** [Markdown with JSON or Mermaid chart specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Plotly JSON, Grafana panel JSON, Mermaid charts, or dashboard panel guidance depending on the user's requested target.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; changelog released 2026-05-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
