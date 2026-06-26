## Description: <br>
Fetch weather data for construction scheduling, including historical data, forecasts, and risk assessment for outdoor work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phucanh08](https://clawhub.ai/user/phucanh08) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Construction planners, project managers, and engineers use this skill to fetch forecast or historical weather data and assess whether outdoor work such as concrete pours, crane work, painting, roofing, or earthwork is workable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups send site coordinates and date ranges to Open-Meteo. <br>
Mitigation: Use only location and schedule data you are comfortable sharing with Open-Meteo and follow project privacy requirements. <br>
Risk: The Python examples rely on local dependencies such as requests and pandas. <br>
Mitigation: Review and install dependencies in a controlled environment before running the examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phucanh08/weather-api-1) <br>
- [Open-Meteo API](https://open-meteo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and concise planning guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Open-Meteo API calls, tabular weather summaries, and construction weather-risk recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
