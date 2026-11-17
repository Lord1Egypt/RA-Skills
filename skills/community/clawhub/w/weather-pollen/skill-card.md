## Description:

Provides weather and pollen reports using free APIs for Anna, TX or a configured weather location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to retrieve current weather, daily forecast, and pollen conditions for Anna, TX or a configured weather location. Operators should treat the user-supplied location argument as display text unless matching coordinates are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can label fixed Anna, TX or configured weather and pollen data as if it came from another requested location.

Mitigation: Configure WEATHER_LAT, WEATHER_LON, and WEATHER_LOCATION for the intended location, and do not rely on the location argument for true location-based results until the skill adds geocoding or clearer fixed-location behavior.

## Reference(s):

- [ClawHub Weather Pollen Skill Page](https://clawhub.ai/thesethrose/skills/weather-pollen)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Pollen.com Current Pollen Forecast](https://www.pollen.com/forecast/current/pollen/75409)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown-formatted weather and pollen report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return weather-only text when includePollen is false; requires network access to external weather and pollen APIs.]

## Skill Version(s):

1.0.3 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
