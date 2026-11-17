## Description:

Provides U.S. weather forecasts from the National Weather Service with global fallback via wttr.in, including accumulation estimates, watches and warnings, hourly detail, AQI, observations, astronomical times, aviation forecasts, and fire weather information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patelhiren](https://clawhub.ai/user/patelhiren)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer weather questions for U.S. locations with NWS data and for non-U.S. locations through the global fallback. It is useful for forecasts, storm timing, precipitation accumulation, severe weather alerts, AQI, observed conditions, astronomical timing, aviation TAFs, and fire weather summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather locations, including precise addresses or ZIP codes if entered, are sent to external weather and geocoding services.

Mitigation: Use city, region, or less precise location text when exact addresses are not necessary.

Risk: AIRNOW_API_KEY is optional but is used in AirNow API requests when configured.

Mitigation: Configure AIRNOW_API_KEY only when AQI data is needed, store it as a secret, and rotate it according to local credential policy.

Risk: Weather, aviation, fire weather, and severe-alert summaries may be incomplete, delayed, or unavailable from upstream services.

Mitigation: Verify safety-critical decisions against official weather, aviation, fire, or emergency-management sources before acting.

## Reference(s):

- [Weather NWS skill page](https://clawhub.ai/patelhiren/skills/weather-nws)
- [National Weather Service API](https://api.weather.gov/)
- [AirNow API key request](https://docs.airnowapi.org/account/request/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style terminal text with structured forecast sections, alerts, optional AQI guidance, and example shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external API-derived weather, air quality, aviation, astronomical, and fire weather data; AQI reliability can depend on optional AIRNOW_API_KEY configuration.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
