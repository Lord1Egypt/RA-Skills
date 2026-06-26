## Description: <br>
Provides configured-location weather reports and optional pollen forecasts using free APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to answer weather and allergy questions for Anna, TX or another location configured through environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may display a requested location name while using configured coordinates and a built-in Anna, TX pollen ZIP code. <br>
Mitigation: Confirm or update WEATHER_LAT, WEATHER_LON, WEATHER_LOCATION, and pollen configuration before relying on results for a different location. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TheSethRose/weather-pollen) <br>
- [Publisher Profile](https://clawhub.ai/user/TheSethRose) <br>
- [Pollen.com Forecast Reference](https://www.pollen.com/forecast/current/pollen/75409) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes current weather, same-day forecast values, precipitation, and optional pollen index details when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: package.json and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
