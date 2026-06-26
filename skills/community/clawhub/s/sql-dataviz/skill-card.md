## Description: <br>
SQL Dataviz helps agents convert SQL query results and tabular data into static charts, interactive HTML charts, and dashboards for reports and web content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqlskills](https://clawhub.ai/user/sqlskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to choose chart types, generate embeddable visualizations from SQL query results, and assemble dashboards or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python charting dependencies may change over time or introduce supply-chain risk in production environments. <br>
Mitigation: Install the skill in a virtual environment and review or pin dependencies before production use. <br>
Risk: Generated HTML charts may rely on CDN-backed Chart.js or Plotly assets, which can expose sensitive chart content patterns and may not work offline. <br>
Mitigation: Use local Chart.js or Plotly assets when charts contain sensitive data or must be available in offline or controlled environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sqlskills/sql-dataviz) <br>
- [Installation](artifact/references/INSTALLATION.md) <br>
- [Integration Guide](artifact/references/INTEGRATION_GUIDE.md) <br>
- [Chart Selection](artifact/references/chart-selection.md) <br>
- [Dashboard](artifact/references/dashboard.md) <br>
- [Plotly Interactive Charts](artifact/references/plotly-interactive.md) <br>
- [Canvas Rendering](artifact/references/canvas-render.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; generated chart assets may be base64 PNG/SVG or self-contained HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create dashboard HTML files or embeddable image strings; Plotly or Chart.js outputs can reference CDN assets unless configured for local assets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
