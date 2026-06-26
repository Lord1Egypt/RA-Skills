## Description: <br>
查询天气预报，支持城市名或坐标，提供当前天气、未来3天预报和天气图标。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greenteawater](https://clawhub.ai/user/greenteawater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask the agent for current weather and a short forecast by city, pinyin, coordinates, or default IP-based location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups are sent to wttr.in and may reveal a requested city or an IP-based location. <br>
Mitigation: Provide an explicit city or coordinate when possible and avoid invoking the skill for sensitive location queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/greenteawater/weather-forecasts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown text with weather values and optional inline SVG icon links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes current conditions, temperature, feels-like temperature, humidity, wind speed, wind direction, and a 3-day forecast.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
