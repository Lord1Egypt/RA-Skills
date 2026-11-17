## Description:

天气查询：使用和风天气（JWT+Host）获取实时天气与未来预报；支持城市名/LocationID/经纬度；缺省地点可用 QWEATHER_DEFAULT_LOCATION。

This skill is ready for commercial/non-commercial use.

## Publisher:

[murphys7017](https://clawhub.ai/user/murphys7017)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to answer current weather and forecast questions from a city name, LocationID, or latitude/longitude. It supports default-location configuration and returns concise weather conditions, temperature, humidity, wind, observation time, and forecast highlights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location queries may be sent to external weather services, including an Open-Meteo fallback path.

Mitigation: Use the skill only where sending queried locations to external weather services is acceptable, and remove or gate the Open-Meteo fallback unless users opt in.

Risk: A token generation utility can print live QWeather JWTs when run.

Mitigation: Do not run token generation in logged environments unless the utility is changed to redact tokens.

Risk: The artifact includes a private-key-shaped placeholder file for QWeather setup.

Mitigation: Replace the placeholder with setup documentation and keep real QWeather private keys outside the skill package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/murphys7017/skills/qweather)
- [QWeather Geo API endpoint](https://geoapi.qweather.com/v2/city/lookup)
- [QWeather current weather endpoint](https://devapi.qweather.com/v7/weather/now)
- [Open-Meteo geocoding endpoint](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo forecast endpoint](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [Structured weather results and concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns current conditions, forecasts, location resolution results, warnings, hourly data, precipitation, and lifestyle indices depending on the invoked tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
