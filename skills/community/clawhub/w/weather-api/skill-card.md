## Description: <br>
Fetch weather data for construction scheduling. Historical data, forecasts, and risk assessment for outdoor work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction project teams and developers use this skill to fetch forecast or historical weather data and assess outdoor workability risks for scheduling decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Site coordinates sent to Open-Meteo may disclose sensitive project locations. <br>
Mitigation: Use only the location precision needed for the analysis and avoid sharing sensitive exact coordinates unless required. <br>
Risk: The skill may read or export project files supplied by the user. <br>
Mitigation: Provide only files needed for weather-risk analysis and review any Excel, CSV, or JSON export before sharing. <br>
Risk: Weather-risk recommendations depend on external weather data and fixed activity thresholds. <br>
Mitigation: Treat outputs as scheduling support and have qualified project staff verify decisions before changing work plans. <br>


## Reference(s): <br>
- [Weather Api ClawHub Listing](https://clawhub.ai/datadrivenconstruction/weather-api) <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>
- [Open-Meteo API](https://open-meteo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, API calls, guidance] <br>
**Output Format:** [Markdown with structured tables and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May offer Excel, CSV, or JSON exports when relevant.] <br>

## Skill Version(s): <br>
2.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
