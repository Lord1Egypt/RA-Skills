## Description:

中文天气查询工具 - 使用中国天气网获取实时天气（无需API密钥，不依赖大模型）

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenera](https://clawhub.ai/user/kenera)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to answer Chinese-language weather questions for supported Chinese cities by running a local Python script that fetches and formats Weather.com.cn data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses the Python requests package.

Mitigation: Pin requests to a reviewed version when stronger supply-chain control is required.

Risk: The skill contacts Weather.com.cn over the network to fetch weather data.

Mitigation: Use the skill only for explicit weather queries and deploy it in environments where outbound access to Weather.com.cn is acceptable.

Risk: Weather data and lifestyle indices may be delayed or general-purpose guidance.

Mitigation: Treat returned weather and lifestyle-index text as informational and verify critical decisions against an authoritative weather source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenera/skills/weather-zh)
- [中国天气网](https://www.weather.com.cn/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text output with Chinese weather details and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and the requests package; contacts Weather.com.cn for weather data.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
