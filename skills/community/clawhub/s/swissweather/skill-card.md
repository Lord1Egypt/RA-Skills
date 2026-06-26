## Description: <br>
Get current weather and forecasts from MeteoSwiss (official Swiss weather service). Use when querying Swiss weather data, local measurements from Swiss weather stations, or Swiss-specific forecasts. Provides real-time measurements (temperature, humidity, wind, precipitation, pressure) from 100+ Swiss stations and multi-day forecasts by postal code. Ideal for Swiss locations - more accurate than generic weather services for Switzerland. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xenofex7](https://clawhub.ai/user/xenofex7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query current Swiss weather station measurements and Swiss postal-code forecasts from MeteoSwiss, including JSON output for programmatic workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecast requests share the queried Swiss postal code with MeteoSwiss. <br>
Mitigation: Avoid submitting sensitive location queries when that disclosure is not acceptable, or use current station measurements instead. <br>
Risk: The optional Python scripts depend on the requests package in the user's Python environment. <br>
Mitigation: Install dependencies only from trusted package indexes and run the scripts in a trusted or isolated Python environment. <br>
Risk: The MeteoSwiss forecast endpoint may change or become unstable. <br>
Mitigation: Fall back to the documented current-weather CSV endpoint or check the MeteoSwiss documentation when forecast calls fail. <br>


## Reference(s): <br>
- [MeteoSwiss API Reference](references/api_info.md) <br>
- [Official MeteoSwiss](https://www.meteoschweiz.admin.ch) <br>
- [Swiss Open Government Data Platform](https://data.geo.admin.ch) <br>
- [Current Weather Measurements CSV](https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and optional JSON weather data from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports station-code lookups, station listing, all-station output, postal-code forecasts, and JSON output flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
