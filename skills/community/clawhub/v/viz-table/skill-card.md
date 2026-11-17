## Description:

Reads CSV or JSON data files and generates interactive ECharts HTML visualizations including bar, line, pie, and donut charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpf](https://clawhub.ai/user/charles-lpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to turn local CSV or JSON datasets into browser-viewable charts with a data table, summary statistics, and optional calculated columns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated report's formula feature can execute arbitrary JavaScript in the browser page.

Mitigation: Use only non-sensitive data unless the formula evaluator is replaced with a restricted arithmetic parser.

Risk: The generated HTML loads ECharts from an external CDN.

Mitigation: Pin or bundle the ECharts dependency before use in environments that require dependency control.

Risk: The skill writes a report to /tmp and opens it in a browser automatically.

Mitigation: Review the generated HTML and execution environment before installing or running the skill.

## Reference(s):

- [ECharts 5 CDN](https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js)
- [Viz Table on ClawHub](https://clawhub.ai/charles-lpf/skills/viz-table)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with generated HTML and shell command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local HTML chart report at /tmp/viz-table-output.html and opens it in a browser.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
