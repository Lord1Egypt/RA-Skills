## Description: <br>
Use when a user asks about weather, temperature, forecasts, air quality, UV index, or weather alerts for any location; it returns structured JSON with more data points and does not require an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[splint3r](https://clawhub.ai/user/splint3r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer weather-related user requests by calling a third-party weather wrapper for current conditions, forecasts, air quality, UV index, and severe weather alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries send location text to api.openmeteo-api.com and upstream weather providers. <br>
Mitigation: Avoid precise sensitive locations when they are not needed, and disclose third-party weather API use before deployment in privacy-sensitive settings. <br>
Risk: Location text is embedded in curl URLs. <br>
Mitigation: Encode user-provided location text safely before executing the curl examples. <br>


## Reference(s): <br>
- [Weather Forecast Plus API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/splint3r/weather-forecast-premium) <br>
- [Weather wrapper homepage](https://openmeteo-api.com) <br>
- [Open-Meteo](https://open-meteo.com) <br>
- [wttr.in](https://wttr.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with curl commands and structured JSON weather responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and sends the requested location to api.openmeteo-api.com and upstream weather providers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
