## Description:

自动化质量成本分析工具，支持Excel/CSV多Sheet数据读取、智能列识别、数据清洗、四大分类计算、自动图表选择和HTML报告输出；当用户需要质量成本分析、成本结构拆解、趋势分析或质量成本报告时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality managers, analysts, and operations teams use this skill to analyze quality-cost data from trusted local Excel or CSV files, classify costs into the four standard categories, and generate charts and report-ready findings. It supports structure analysis, trend analysis, anomaly notes, and optimization guidance for quality-cost reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses pickle files for intermediate data, which can be unsafe when loaded from untrusted sources.

Mitigation: Process only trusted local files, verify intermediate files before loading them, or replace the pickle exchange with a safer format such as CSV, JSON, or Parquet.

Risk: Generated HTML reports and charts may load Plotly JavaScript from a remote CDN, which can expose sensitive report use to external network dependencies.

Mitigation: Remove, pin, or self-host the Plotly dependency before opening reports that contain sensitive business data.

Risk: The advertised report-generation step depends on an empty report generator script in the submitted artifact.

Mitigation: Review and complete the report-generation implementation, or use the provided HTML template through a verified rendering path before relying on one-click report output.

## Reference(s):

- [Quality cost analysis framework](artifact/references/quality_cost_framework.md)
- [Chart selection rules](artifact/references/chart_selection_rules.md)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-quality-cost-analysis)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)
- [Server-resolved GitHub repository](https://github.com/duding-engicool/skill-quality-cost-analysis)
- [Server-resolved GitHub commit](https://github.com/duding-engicool/skill-quality-cost-analysis/commit/bd9785da8b89844d09c36f582d6f23b9c08a8334)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples; generated artifacts may include pickle, JSON, and HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes trusted local Excel or CSV files and may generate Plotly HTML reports that load JavaScript from a CDN.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
