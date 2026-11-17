## Description:

Global weather queries powered by QWeather, including real-time weather, multi-day forecasts, and trip-friendly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnixner](https://clawhub.ai/user/gnixner)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure QWeather access, resolve city inputs, and query current weather or 3-day and 7-day forecasts for readable weather and trip summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles QWeather API credentials and can create or cache bearer tokens in local files.

Mitigation: Use only an API host copied from the official QWeather console, keep the private key and local directory owner-readable only, and do not commit local files.

Risk: Setup, tests, city lookup fallbacks, and weather queries make network requests and create local state.

Mitigation: Review the skill before installing, run initialization and tests in an appropriate environment, and expect local configuration, cache, and city data files to be created.

## Reference(s):

- [QWeather API documentation](https://dev.qweather.com/docs/api/)
- [QWeather authentication documentation](https://dev.qweather.com/docs/configuration/authentication/)
- [QWeather GeoAPI documentation](https://dev.qweather.com/docs/api/geoapi/)
- [QWeather console](https://console.qweather.com)
- [LocationList](https://github.com/qwd/LocationList)
- [setup.md](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON weather payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied QWeather credentials, a local private key path, and network access to QWeather APIs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
