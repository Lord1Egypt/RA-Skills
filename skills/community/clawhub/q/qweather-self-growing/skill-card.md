## Description: <br>
Global weather queries powered by QWeather, with real-time weather, multi-day forecasts, trip-friendly summaries, and controlled expansion along official API documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnixner](https://clawhub.ai/user/gnixner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query QWeather for current weather, 3-day or 7-day forecasts, and travel-oriented weather summaries. It also guides controlled extensions when a requested QWeather capability is supported by official documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run setup scripts and handle local QWeather credential configuration. <br>
Mitigation: Require the agent to show exact commands and file paths before setup, use a dedicated QWeather credential, keep local/ and key files out of version control, and store the private key with restrictive permissions. <br>
Risk: The self-growing workflow can update skill instructions or behavior after consulting documentation. <br>
Mitigation: Review any proposed SKILL.md or script changes before accepting them, then rerun the bundled setup and smoke tests. <br>
Risk: Weather results depend on external QWeather APIs, local city data, and cached JWT state. <br>
Mitigation: Treat forecasts as time-sensitive, rerun queries before travel decisions, and refresh initialization data when city resolution or API connectivity fails. <br>


## Reference(s): <br>
- [QWeather API Documentation](https://dev.qweather.com/docs/api/) <br>
- [QWeather Authentication Documentation](https://dev.qweather.com/docs/configuration/authentication/) <br>
- [QWeather GeoAPI Documentation](https://dev.qweather.com/docs/api/geoapi/) <br>
- [QWeather Console](https://console.qweather.com) <br>
- [LocationList](https://github.com/qwd/LocationList) <br>
- [Setup Reference](references/setup.md) <br>
- [Publish Reference](references/publish.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON weather output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can present brief, trip-oriented, or raw JSON weather results; setup writes local credential configuration and cache files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
