## Description:

天气播报格式化技能。当用户询问天气、查看天气预报、或需要生成天气报告时触发。技能包含完整的天气信息格式化模板，支持今天/明天/后天三种类型，以及时间段的斜体规则。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhjx94264](https://clawhub.ai/user/zhjx94264)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch weather data and format Chinese weather reports for today, tomorrow, or the day after tomorrow. It provides markdown tables, emoji conventions, summary bullets, and rules for italicizing elapsed time periods in same-day reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt the agent to make an outbound request to wttr.in for weather data.

Mitigation: Install only where that public weather-data request is acceptable, or modify the template to use an approved weather-data integration.

Risk: The report template has a fixed Chinese tone, locale style, and formatting rules.

Mitigation: Review and adapt the template before deployment when another language, location policy, or communication style is required.

## Reference(s):

- [Weather Report Complete Template](references/weather_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown weather report with tables, bullet points, emojis, and optional inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-formatted weather reports using templates for today, tomorrow, and the day after tomorrow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
