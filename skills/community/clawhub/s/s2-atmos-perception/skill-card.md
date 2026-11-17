## Description:

S2-SP-OS Atmos Radar. Real-time meteorological and space weather (NOAA) perception organ for AI Agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve location-based weather, air-quality, and NOAA space-weather signals, then present environmental insights as advice without automatically controlling physical devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Entered locations are sent to Open-Meteo and NOAA is queried for space-weather data.

Mitigation: Ask for the user's location only when needed and disclose the external API queries before use.

Risk: The security evidence says atmos.py currently will not run as valid Python.

Mitigation: Repair and test atmos.py before executing the skill in an agent workflow.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/spacesq/skills/s2-atmos-perception)
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search?name={safe_query}&count=1&format=json)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m)
- [Open-Meteo Air Quality API](https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi)
- [NOAA Space Weather Scales](https://services.swpc.noaa.gov/products/noaa-scales.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown human briefings or JSON agent-mode results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided location and python3; queries Open-Meteo and NOAA web APIs.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
