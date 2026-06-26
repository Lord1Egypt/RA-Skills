## Description: <br>
Monitors weather for any location, checks forecast thresholds for rain, snow, temperature, wind, UV, and pressure, and provides alerts, daily briefings, event suitability checks, and trend summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigas](https://clawhub.ai/user/indigas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to check current and forecast weather, monitor threshold-based conditions, plan events, and receive concise weather alerts for configured locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried or monitored locations may be shared with public weather services. <br>
Mitigation: Install and use only for locations that are acceptable to disclose to the configured public weather APIs. <br>
Risk: Automatic alert delivery or scheduling may depend on host-level exec-event or scheduler integrations outside the script. <br>
Mitigation: Review the host integration and configured notification method before enabling automatic alerts. <br>


## Reference(s): <br>
- [Weather Data Sources](references/weather-sources.md) <br>
- [Open-Meteo](https://open-meteo.com/) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [wttr.in JSON weather endpoint](https://wttr.in/{location}?format=j1) <br>
- [OpenWeatherMap Current Weather API](https://api.openweathermap.org/data/2.5/weather) <br>
- [ClawHub skill page](https://clawhub.ai/indigas/weather-alert) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style weather summaries, alert lists, event suitability guidance, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local configuration, cache forecast data, and query public weather services for requested or monitored locations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
