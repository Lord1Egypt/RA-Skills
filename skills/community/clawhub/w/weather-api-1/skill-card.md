## Description:

Fetch weather data for construction scheduling, including historical data, forecasts, and risk assessment for outdoor work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phucanh08](https://clawhub.ai/user/phucanh08)

### License/Terms of Use:


## Use Case:

External developers and construction teams use this skill to retrieve Open-Meteo weather forecasts or historical data for a jobsite and estimate weather-related workability risks for outdoor construction activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the sample client may send jobsite coordinates and requested dates to Open-Meteo.

Mitigation: Avoid sending sensitive site locations or dates unless the deployment has approved Open-Meteo as an external data processor.

Risk: Construction risk thresholds may not reflect site-specific safety rules or professional judgment.

Mitigation: Treat generated risk assessments as planning support and review them against local safety requirements before scheduling work.

## Reference(s):

- [Open-Meteo API](https://open-meteo.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Python code examples and tabular data structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Open-Meteo with jobsite coordinates and requested dates when the sample client is run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
