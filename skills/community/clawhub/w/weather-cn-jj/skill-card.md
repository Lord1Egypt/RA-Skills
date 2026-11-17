## Description:

国内天气+空气质量查询。支持城市和区县级，中文输出。数据源: wttr.in + Open-Meteo。无需 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujun2508](https://clawhub.ai/user/lujun2508)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Chinese-language current or next-day weather and optional US AQI summaries for supported Chinese cities and districts.

### Deployment Geography for Use:

Global; weather coverage is focused on China.

## Known Risks and Mitigations:

Risk: City or district queries are sent to wttr.in, and AQI requests send coordinates to Open-Meteo.

Mitigation: Invoke the skill only with locations that are acceptable to share with those external weather services.

Risk: Weather or AQI data may be delayed, unavailable, or less precise for district-level locations.

Mitigation: Treat results as informational and verify with an authoritative source before making safety-critical or operational decisions.

Risk: The skill is designed for Chinese output and does not provide a language option.

Mitigation: Use it only in workflows where Chinese-language weather guidance is appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lujun2508/skills/weather-cn-jj)
- [Publisher profile](https://clawhub.ai/user/lujun2508)
- [wttr.in weather endpoint](https://wttr.in/)
- [Open-Meteo Air Quality API endpoint](https://air-quality-api.open-meteo.com/v1/air-quality)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Plain text Chinese weather and AQI summary, with shell command and Python usage guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional AQI and next-day forecast flags; output is designed for Chinese-language use.]

## Skill Version(s):

1.3.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
