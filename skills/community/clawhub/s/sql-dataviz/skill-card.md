## Description:

SQL Dataviz helps agents convert SQL query results and tabular data into static charts, interactive Plotly HTML charts, and dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moniq888](https://clawhub.ai/user/moniq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and reporting agents use this skill to choose chart types, prepare visualization code, install Python charting dependencies, and generate charts or dashboards from SQL-derived data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may modify the user's Python environment and fetch packages from remote package indexes.

Mitigation: Install in an isolated virtual environment, avoid administrator privileges, and review or pin dependencies before use.

Risk: Interactive HTML dashboards should be treated as active web pages and may load Plotly from an external CDN unless bundled locally.

Mitigation: Use locally bundled Plotly when external network access is not acceptable, and review generated HTML before sharing or opening in sensitive environments.

Risk: Generated charts, dashboards, and reports may expose sensitive SQL result data.

Mitigation: Redact or aggregate sensitive data before generating or distributing visualizations.

Risk: Persistent pip mirror configuration can affect future Python package installations.

Mitigation: Set package mirrors only intentionally and document or revert the configuration after use.

## Reference(s):

- [SQL Dataviz ClawHub page](https://clawhub.ai/moniq888/skills/sql-dataviz)
- [Chart Selection](artifact/references/chart-selection.md)
- [Installation Guide](artifact/references/INSTALLATION.md)
- [Integration Guide](artifact/references/INTEGRATION_GUIDE.md)
- [Plotly Interactive Charts](artifact/references/plotly-interactive.md)
- [Dashboard Guide](artifact/references/dashboard.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; generated visualization artifacts may be base64 PNG strings or interactive HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on Python visualization dependencies and may produce active HTML dashboards.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
