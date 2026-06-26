## Description: <br>
中国天气预报查询 - 基于中国天气网(weather.com.cn)获取7天天气预报和生活指数数据。纯 Python 实现，无需 API Key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoopan007](https://clawhub.ai/user/hoopan007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer China-focused weather questions, including 7-day forecasts and daily life index guidance for supported Chinese cities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends queried city names to weather.com.cn and depends on that external service for weather data. <br>
Mitigation: Use it only for intended Chinese city weather lookups and avoid submitting sensitive or unrelated query text. <br>
Risk: Weather data may be delayed or unavailable if weather.com.cn changes, is unreachable, or returns incomplete data. <br>
Mitigation: Treat results as informational guidance and verify important weather-sensitive decisions with an authoritative source. <br>
Risk: The skill is intended to run a bundled local Python script. <br>
Mitigation: Approve only the expected python3 weather lookup commands and do not approve unrelated shell commands under this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoopan007/weather-china) <br>
- [中国天气网](https://www.weather.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text weather summaries or structured JSON from a local Python command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and network access to weather.com.cn; no API key is required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
