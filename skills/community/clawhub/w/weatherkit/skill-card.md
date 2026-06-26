## Description: <br>
Access Apple WeatherKit REST API for detailed weather forecasts using JWT authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmcq](https://clawhub.ai/user/jimmcq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to retrieve current and forecast weather data from Apple WeatherKit for a latitude and longitude. It is useful when workflows need detailed weather fields such as UV index, humidity, wind, sunrise and sunset times, or multi-day forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a WeatherKit-specific Apple private key. <br>
Mitigation: Keep the .p8 key outside shared folders, restrict file permissions, and rotate the key if exposure is suspected. <br>
Risk: Forecast requests and debug output can expose sensitive location information. <br>
Mitigation: Avoid sharing stderr logs when queried locations are sensitive and review logs before disclosure. <br>


## Reference(s): <br>
- [Apple WeatherKit REST API Documentation](https://developer.apple.com/documentation/weatherkitrestapi/) <br>
- [ClawHub WeatherKit Skill Page](https://clawhub.ai/jimmcq/weatherkit) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON forecast data, with command-line usage guidance and stderr diagnostics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Apple WeatherKit credentials in environment variables and sends latitude/longitude requests to Apple WeatherKit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
