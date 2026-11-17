## Description:

全球城市天气查询与对比工具，支持中英文城市名、多语言输出、Open-Meteo 数据源和大城市定位。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redapp](https://clawhub.ai/user/redapp)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer single-city weather questions or compare weather across cities in Chinese or English. It is useful for current conditions, temperature ranges, precipitation likelihood, and simple travel guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried city names are sent over HTTPS to Open-Meteo for geocoding and weather results.

Mitigation: Use this skill only where sharing requested city names with Open-Meteo is acceptable.

Risk: Weather answers depend on live Open-Meteo availability and returned data.

Mitigation: Treat results as current guidance and re-query or cross-check for critical travel decisions.

## Reference(s):

- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [ClawHub skill page](https://clawhub.ai/redapp/skills/whale-weather)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands]

**Output Format:** [Plain text weather report with bilingual labels and short advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries may call Open-Meteo over HTTPS for geocoding and weather data.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
