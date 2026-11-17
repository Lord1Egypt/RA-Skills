## Description:

中国天气预报查询基于中国天气网(weather.com.cn)获取7天天气预报和生活指数数据，纯 Python 实现且无需 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoopan007](https://clawhub.ai/user/hoopan007)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer China-focused weather questions, including today's weather, rain expectations, weekly forecasts, umbrella needs, and clothing guidance for supported Chinese cities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a Python script through exec and makes live HTTPS requests to China Weather services.

Mitigation: Review the command before execution and run it only in environments where outbound access to those services is expected.

Risk: Weather results depend on live China Weather service availability and may be delayed.

Mitigation: Use the output as best-effort weather guidance and verify critical decisions against an authoritative forecast source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hoopan007/skills/weather-china)
- [China Weather](https://www.weather.com.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Formatted text or JSON weather forecast output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes city name, city code, query time, data source, 7-day forecast, and life indices when available.]

## Skill Version(s):

1.0.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
