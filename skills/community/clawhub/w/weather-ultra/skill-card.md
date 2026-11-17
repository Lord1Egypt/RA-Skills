## Description:

Weather Ultra retrieves weather, air quality, sunrise and sunset times, golden and blue hour windows, and sunrise or sunset glow forecasts for a requested city.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pazzilivo](https://clawhub.ai/user/pazzilivo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, photographers, and outdoor planners use this skill to check city weather, air quality, daylight timing, golden and blue hour windows, and sunrise or sunset color quality before planning shoots or outdoor activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sources ~/.openclaw/.env before running its weather script.

Mitigation: Review the script before installation and configure only the required WEATHERAPI_KEY and SUNSETHUE_KEY values instead of relying on broad environment sourcing.

Risk: City names and resolved coordinates are sent to WeatherAPI and SunsetHue.

Mitigation: Disclose the external API use to users and avoid entering sensitive locations when privacy is a concern.

Risk: The release evidence marks the security verdict as suspicious because user-facing scoping and disclosure are incomplete.

Mitigation: Document required API keys, external services, expected data sharing, and narrower trigger phrases before broad deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pazzilivo/skills/weather-ultra)
- [Publisher Profile](https://clawhub.ai/user/pazzilivo)
- [WeatherAPI forecast endpoint](https://api.weatherapi.com/v1/forecast.json?key=${WEATHERAPI_KEY}&q=${CITY}&days=${DAYS}&lang=zh&aqi=yes)
- [SunsetHue sunrise event endpoint](https://api.sunsethue.com/event?latitude=${LAT}&longitude=${LON}&date=${DATE}&type=sunrise&key=${SUNSETHUE_KEY})
- [SunsetHue sunset event endpoint](https://api.sunsethue.com/event?latitude=${LAT}&longitude=${LON}&date=${DATE}&type=sunset&key=${SUNSETHUE_KEY})

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text weather and photography-light report emitted by a Bash script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a city name and optional day count; output includes weather, air quality, sunrise and sunset times, golden and blue hour windows, and glow quality ratings.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
