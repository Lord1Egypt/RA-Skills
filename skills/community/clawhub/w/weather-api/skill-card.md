## Description:

Fetch weather data for construction scheduling, including historical data, forecasts, and risk assessment for outdoor work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction project managers, schedulers, and developers use this skill to fetch weather conditions, assess outdoor workability, and plan construction activities around forecast or historical weather risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask the agent to read user-provided file paths and create exports, which can expose sensitive project or credential files if paths are broad.

Mitigation: Review before installation, scope file access to intended project or weather input directories, and avoid credential or configuration files.

Risk: The skill makes network weather lookups through a public weather API, so outputs depend on external service availability and returned data quality.

Mitigation: Validate inputs and weather outputs before using recommendations for construction scheduling decisions.

## Reference(s):

- [Weather Api ClawHub listing](https://clawhub.ai/datadrivenconstruction/skills/weather-api)
- [Data Driven Construction](https://datadrivenconstruction.io)
- [Open-Meteo API](https://open-meteo.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown tables and summaries with Python code examples and optional CSV, Excel, or JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include weather summaries, risk levels, workable-hour estimates, affected activities, recommendations, and export options.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
