## Description: <br>
Weather Pulse queries current weather, 3-30 day daily forecasts, 24-168 hour hourly forecasts, lifestyle indices, air quality, pollutant measurements, and 7-day pollutant forecasts by city name, coordinates, CityId, or WAQI ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etmnb](https://clawhub.ai/user/etmnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch weather, forecast, lifestyle-index, and air-quality data from QWeather and WAQI using user-provided credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires user-provided QWeather and/or WAQI credentials. <br>
Mitigation: Store credentials in environment variables or a private secret store, and avoid committing keys to scripts or shared files. <br>
Risk: Queried city names, coordinates, and WAQI 'here' lookups are sent to third-party weather providers. <br>
Mitigation: Use the skill only when sharing the queried location with QWeather or WAQI is acceptable for the use case. <br>
Risk: Using an incorrect QWeather API host can send requests to the wrong endpoint or fail authentication. <br>
Mitigation: Copy QWEATHER_API_HOST only from the QWeather console for the configured project. <br>


## Reference(s): <br>
- [Weather Pulse on ClawHub](https://clawhub.ai/etmnb/weather-pulse) <br>
- [QWeather documentation](https://dev.qweather.com/docs) <br>
- [QWeather getting started](https://dev.qweather.com/docs/start/) <br>
- [QWeather pricing](https://dev.qweather.com/docs/finance/pricing/) <br>
- [WAQI API documentation](https://aqicn.org/api/) <br>
- [WAQI city lookup](https://aqicn.org/city/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration guidance] <br>
**Output Format:** [Plain text or JSON from command-line weather and air-quality queries, with Markdown setup guidance in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QWeather credentials for weather endpoints and a WAQI token for air-quality endpoints.] <br>

## Skill Version(s): <br>
1.3.6 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
