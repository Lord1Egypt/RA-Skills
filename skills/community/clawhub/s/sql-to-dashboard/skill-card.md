## Description:

Converts supplied SQL queries or query results into chart recommendations and dashboard specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to turn supplied SQL queries or result sets into chart recommendations and renderable specs for Plotly, Grafana, or Mermaid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Very large result sets may be summarized through aggregation or sampling, which can hide outliers or change the apparent distribution.

Mitigation: Review any stated aggregation or sampling choice and confirm it matches the analysis goal before using the chart.

Risk: Chart recommendations can be misleading when based only on an inferred query shape rather than actual result values.

Mitigation: Provide representative result rows when possible and review the selected chart type plus column-to-axis mappings.

Risk: Some support files reference an older skill name, which can confuse installation or maintenance workflows.

Mitigation: Verify release, install, and test references use the current sql-to-dashboard slug before publishing or operational use.

## Reference(s):

- [Skill reference index](references/index.md)
- [Metadata source link](https://github.com/MiniMax-AI/skills)
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/sql-to-dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with JSON or Mermaid code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Plotly JSON, Grafana panel JSON, Mermaid chart blocks, and column-to-axis mappings; should not invent data points.]

## Skill Version(s):

1.0.1 (source: server release metadata and CHANGELOG, released 2026-05-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
