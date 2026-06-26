## Description: <br>
Fetch historical or forecast weather by location or coordinates via Open-Meteo. No API key needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minshi-veyt](https://clawhub.ai/user/minshi-veyt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can fetch recent historical weather or near-term forecasts for a named location or latitude/longitude coordinates. The skill is suited for weather checks, precipitation review, and garden-planning workflows that use evapotranspiration and crop coefficient calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location names and coordinates are sent to Open-Meteo for geocoding and weather lookup. <br>
Mitigation: Avoid entering locations or coordinates that should remain private. <br>
Risk: The skill runs local Python scripts and installs Python dependencies. <br>
Mitigation: Use a virtual environment and review dependencies before execution. <br>
Risk: Weather results depend on live Open-Meteo availability and returned data quality. <br>
Mitigation: Retry transient failures and review outputs before using them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minshi-veyt/weather-loader) <br>
- [Open-Meteo](https://open-meteo.com/) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude={lat}) <br>
- [Open-Meteo historical archive API](https://archive-api.open-meteo.com/v1/archive?latitude={lat}) <br>
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON] <br>
**Output Format:** [CSV or JSON weather data printed to stdout, with status and error messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to Open-Meteo; accepts location or latitude/longitude, days, crop coefficient, and output format parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
