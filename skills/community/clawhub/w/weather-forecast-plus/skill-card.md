## Description:

Use when a user asks about weather, temperature, forecasts, air quality, UV index, or weather alerts for any location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urianpaul94](https://clawhub.ai/user/urianpaul94)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current weather, multi-day forecasts, air quality, UV index, severe weather alerts, and concise weather summaries for user-specified locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location text is substituted into shell commands for remote API calls.

Mitigation: Review generated commands before execution and use structured HTTP query parameters or safe URL encoding for location values.

Risk: The skill may write weather_cache.json containing weather responses plus the local username and machine name when local caching is requested.

Mitigation: Make caching opt-in, avoid storing host identifiers, and delete cache files when they are no longer needed.

Risk: Weather requests rely on a third-party aggregation service and upstream weather providers.

Mitigation: Disclose the intermediary service to users and verify that its availability, terms, and privacy posture fit the deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/urianpaul94/skills/weather-forecast-plus)
- [Weather Forecast Plus API Reference](references/api.md)
- [Weather Forecast Plus homepage](https://openmeteo-api.com)
- [Open-Meteo API](https://open-meteo.com)
- [wttr.in](https://wttr.in)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with curl commands and JSON weather responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write weather_cache.json when the API response requests local caching. Requires curl.]

## Skill Version(s):

4.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
