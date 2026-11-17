## Description:

Get current weather and forecasts via wttr.in or Open-Meteo for user-specified locations, with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer weather, temperature, rain, and forecast questions for cities, regions, or airport codes. It is intended for routine current-condition and forecast lookups, not historical weather, severe weather alerts, climate analysis, aviation, or marine weather.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather location queries may be sent to wttr.in over unencrypted HTTP in the artifact examples.

Mitigation: Prefer HTTPS endpoints and avoid sending sensitive private location or travel details in weather lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/weather-forecast-ai)
- [wttr.in help](https://wttr.in/:help)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and weather lookup examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl command examples that request text, JSON, or PNG weather formats from wttr.in.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
