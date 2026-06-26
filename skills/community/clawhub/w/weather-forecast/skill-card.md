## Description: <br>
This skill retrieves hourly weather forecasts and temperature data for requested locations using the Open-Meteo API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex098929](https://clawhub.ai/user/alex098929) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer weather and temperature questions for named places or coordinates, including current and future hourly forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries may send requested locations or coordinates to Open-Meteo. <br>
Mitigation: Use city-level or approximate locations when privacy matters, and avoid precise current-location coordinates unless needed. <br>


## Reference(s): <br>
- [Weather Forecast on ClawHub](https://clawhub.ai/alex098929/weather-forecast) <br>
- [Open-Meteo API Response Format](references/api_response_format.md) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Natural-language weather summary with optional script output and JSON data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses latitude and longitude inputs and returns hourly Celsius temperature forecasts by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
