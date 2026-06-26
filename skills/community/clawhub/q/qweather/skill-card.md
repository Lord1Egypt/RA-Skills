## Description: <br>
Queries real-time weather and forecasts through QWeather with JWT and host configuration, supporting city names, LocationID values, coordinates, and an optional default location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[murphys7017](https://clawhub.ai/user/murphys7017) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to answer weather questions without general web search by resolving a city, LocationID, or coordinates and returning current conditions or daily forecasts. It is intended for agents that can call local JavaScript weather helpers configured with QWeather credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local QWeather credential configuration and can generate JWTs from an Ed25519 private key. <br>
Mitigation: Configure credentials locally, protect private key files, and avoid running or sharing output from the JWT token helper. <br>
Risk: Weather location queries are sent to external weather services, including an under-documented Open-Meteo fallback path. <br>
Mitigation: Use only when sending requested locations to QWeather and Open-Meteo is acceptable, and disclose the fallback provider before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/murphys7017/qweather) <br>
- [QWeather Geo API endpoint](https://geoapi.qweather.com/v2/city/lookup) <br>
- [QWeather weather API endpoint](https://devapi.qweather.com/v7/weather/now) <br>
- [Open-Meteo geocoding fallback endpoint](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo forecast fallback endpoint](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON objects with weather fields and concise natural-language guidance for missing configuration or request failures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns resolved location, current weather, forecast details, source labels, and structured error messages when configuration or API calls fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
