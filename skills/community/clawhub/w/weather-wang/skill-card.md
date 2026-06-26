## Description: <br>
Queries weather forecasts for a specified city or region, including temperature, conditions, precipitation probability, wind, air quality, ultraviolet index, alerts, and multi-day outlooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[congwupiece](https://clawhub.ai/user/congwupiece) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve current and upcoming weather information for planning travel, outdoor activity, daily preparation, and weather-sensitive decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location queries may be sent to the configured weather service. <br>
Mitigation: Avoid sending sensitive or unnecessary location detail, and use only weather providers approved for the deployment environment. <br>
Risk: Weather information can be incomplete, delayed, or insufficient for severe-weather and safety-critical decisions. <br>
Mitigation: Verify severe-weather alerts and safety-critical travel decisions with an official weather source before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/congwupiece/weather-wang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown weather report with optional structured JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include current weather, forecast highlights, alerts, and travel or safety suggestions based on returned weather data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
