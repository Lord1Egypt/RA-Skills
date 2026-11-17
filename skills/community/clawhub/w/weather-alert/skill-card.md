## Description:

Proactive weather monitoring and alerting that tracks conditions for any location, sends threshold-based notifications for rain, snow, temperature, wind, UV, and pressure, and provides daily briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigas](https://clawhub.ai/user/indigas)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check current weather, receive 7-day briefings, monitor configurable weather thresholds, and assess outdoor event suitability for selected locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location data is sent to third-party weather services.

Mitigation: Review the data-sharing implications before installation and use locations that are appropriate to disclose to the configured weather providers.

Risk: The automated alert configuration includes an execution-style notification method.

Mitigation: Do not enable `exec-event` unless the host clearly shows what will run, how often it runs, where state is stored, and how to turn it off.

Risk: Install and persistence disclosures are not tight enough for unattended operation.

Mitigation: Use a pinned or trusted installer and review scheduled checks, local state paths, and shutdown controls before enabling automated monitoring.

## Reference(s):

- [Weather Data Sources](artifact/references/weather-sources.md)
- [Open-Meteo](https://open-meteo.com/)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [wttr.in JSON weather endpoint](https://wttr.in/{location}?format=j1)
- [OpenWeatherMap weather API](https://api.openweathermap.org/data/2.5/weather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text weather reports, alert summaries, event-suitability notes, shell command examples, and YAML configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live third-party weather API results, cached weather data, configurable thresholds, and location-specific alert output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
