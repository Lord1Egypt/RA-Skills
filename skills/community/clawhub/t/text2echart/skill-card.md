## Description:

text2echart generates ECharts chart configurations and HTML, SVG, or PNG outputs from CSV, JSON, or explicit chart requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifeel-is-a-mouse](https://clawhub.ai/user/ifeel-is-a-mouse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use text2echart to turn CSV/JSON data or explicit chart requests into ECharts visualizations for reports, previews, and local export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted chart input can execute scripts in generated chart HTML.

Mitigation: Use only trusted chart data and JSON, and treat generated chart HTML as executable content before opening or sharing it.

Risk: Screenshot and SVG rendering depend on Playwright and use temporary HTML files.

Mitigation: Pin Playwright when installing screenshot support, prefer offline/embed mode for sensitive data, and review generated files before rendering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ifeel-is-a-mouse/skills/text2echart)
- [Prompt guide](prompt.md)
- [ECharts option reference](references/echarts-option-reference.md)
- [ECharts Chinese option reference](references/echarts-option-zh.md)
- [ECharts wordcloud reference](references/echarts-wordcloud.md)
- [Apache ECharts option documentation](https://echarts.apache.org/en/option.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown responses containing ECharts option JSON, HTML code blocks, CLI commands, and generated HTML/SVG/PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports browser preview and offline embedded HTML; screenshot and standalone SVG extraction require Playwright.]

## Skill Version(s):

2.3.11 (source: SKILL.md metadata and server release metadata; artifact/package.json reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
