## Description:

Get weather, air quality, sunrise and sunset times, golden and blue hour windows, and sunrise or sunset glow quality forecasts for a requested city.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pazzilivo](https://clawhub.ai/user/pazzilivo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve city-level weather, air quality, daylight timing, golden or blue hour windows, and sunrise or sunset glow quality for photography and outdoor planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends city or location-derived coordinates to WeatherAPI and Sunsethue.

Mitigation: Use only when sharing the requested location with those services is acceptable.

Risk: The skill loads local secrets from ~/.openclaw/.env in a way that can run unintended shell code or expose API keys.

Mitigation: Review before installing and prefer passing WEATHERAPI_KEY and SUNSETHUE_KEY from a controlled environment.

## Reference(s):

- [Weather Pro on ClawHub](https://clawhub.ai/pazzilivo/skills/weather-pro)
- [pazzilivo ClawHub Profile](https://clawhub.ai/user/pazzilivo)
- [wttr.in Help](https://wttr.in/:help)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text weather report with city, date, temperature, wind, conditions, humidity, PM2.5, sunrise and sunset, golden and blue hour windows, and glow quality scores.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq. WEATHERAPI_KEY and SUNSETHUE_KEY are optional environment variables used when calling external weather and glow forecast services.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
