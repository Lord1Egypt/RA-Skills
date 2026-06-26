## Description: <br>
Use when users ask about weather conditions, forecasts, or climate information for locations in China. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JaceyMarvin99](https://clawhub.ai/user/JaceyMarvin99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve current weather, air quality, weather alerts, and multi-day forecasts for locations in China. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location weather queries are sent to the 60s.viki.moe weather service. <br>
Mitigation: Avoid entering sensitive personal details in location fields and use only the minimum location needed for the weather request. <br>
Risk: The skill invokes local bash scripts that run curl requests to an external API. <br>
Mitigation: Review the scripts before installation or execution and run them only in environments where outbound weather API calls are acceptable. <br>


## Reference(s): <br>
- [Weather Query on ClawHub](https://clawhub.ai/JaceyMarvin99/weather-query) <br>
- [60s Weather API](https://60s.viki.moe/v2/weather) <br>
- [60s Weather Forecast API](https://60s.viki.moe/v2/weather/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown, plain text, or JSON returned by shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast queries accept a location, optional output encoding, and an optional 0-8 day forecast range.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
