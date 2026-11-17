## Description:

基于质量月度数据生成专业的质量月报；当用户需要生成质量月报、汇总月度测试成果、进行多月数据对比分析时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers, test leads, and delivery teams use this skill to convert monthly quality data from Excel, JSON, or manual input into a structured quality report with metrics, trend analysis, PDCA summaries, and visual charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may auto-install dependencies for Excel parsing and chart rendering.

Mitigation: Run it in a scoped workspace and require approval before dependency installation.

Risk: Generated HTML may include unsafe content derived from report data.

Mitigation: Use trusted source files, escape or sanitize report inputs before rendering, and treat generated HTML as potentially active content until reviewed.

Risk: Untrusted Excel or Markdown inputs can affect parsing and report output.

Mitigation: Avoid untrusted inputs, validate files against the documented data format, and review generated reports before sharing.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/duding-engicool/skill-quality-monthly-report)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-quality-monthly-report)
- [Data format specification](artifact/references/data_format.md)
- [Analysis framework](artifact/references/analysis_framework.md)
- [Report template](artifact/assets/report_template.md)
- [Outline template](artifact/reports/outline_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report content, JSON metric output, and a generated HTML report file with SVG charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one HTML quality monthly report after the user confirms the report outline.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
