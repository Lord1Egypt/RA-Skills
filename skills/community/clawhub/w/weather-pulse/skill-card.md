## Description:

Weather Pulse helps agents query current weather, daily and hourly forecasts, lifestyle indices, and air quality for locations provided as city names, coordinates, CityIds, or WAQI IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etmnb](https://clawhub.ai/user/etmnb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve weather, forecast, lifestyle-index, and air-quality data from QWeather and WAQI during user-facing weather lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A QWeather API key and searched location may be sent to any host configured in QWEATHER_API_HOST.

Mitigation: Set QWEATHER_API_HOST only to the exact host from the QWeather console and use dedicated low-quota API keys.

Risk: QWeather and WAQI receive the locations queried through the skill.

Mitigation: Avoid submitting sensitive precise locations when a broader city-level query is sufficient.

Risk: Credential storage in shared .env files can increase exposure.

Mitigation: Prefer environment variables and keep API credentials out of committed or shared files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/etmnb/skills/weather-pulse)
- [QWeather Documentation](https://dev.qweather.com/docs)
- [QWeather Getting Started](https://dev.qweather.com/docs/start/)
- [QWeather Pricing](https://dev.qweather.com/docs/finance/pricing/)
- [WAQI API Documentation](https://aqicn.org/api/)
- [WAQI City Lookup](https://aqicn.org/city/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Plain text weather and AQI summaries or raw JSON, with Markdown setup guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QWeather and/or WAQI credentials; queried locations are sent to the selected weather or air-quality provider.]

## Skill Version(s):

1.3.6 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
