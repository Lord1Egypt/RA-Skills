## Description:

Generate a TV-style weather infographic with a location-specific seasonal background.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silverkiwi](https://clawhub.ai/user/silverkiwi)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to create a visual weather forecast for a supplied address and coordinates, combining current conditions and a seven-day forecast into a broadcast-style infographic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer modifies the host Python environment.

Mitigation: Review the install command before use and prefer running the skill in an isolated virtual environment.

Risk: Precise address and coordinate inputs may be sent to Gemini and Open-Meteo.

Mitigation: Avoid private street addresses unless that sharing is acceptable; use city-level or rounded-coordinate inputs where possible.

## Reference(s):

- [Weather TV style skill page](https://clawhub.ai/silverkiwi/skills/weather-infographic)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image file path with terminal status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY and sends location details to external weather and image-generation services.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
