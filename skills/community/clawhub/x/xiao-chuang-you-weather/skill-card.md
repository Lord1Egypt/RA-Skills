## Description:

Xiao Chuang You Weather responds to weather-related requests by retrieving current conditions and giving practical clothing, travel, air-quality, and seasonal guidance in a gentle Chinese-language style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcr3344](https://clawhub.ai/user/zcr3344)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill when they ask about weather, temperature, clothing, umbrellas, precipitation, air quality, UV, or travel conditions. The skill provides current-condition summaries, practical living and travel suggestions, and optional 24-solar-term seasonal context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can infer a user's location from prior conversation or MEMORY.md and send it to a third-party weather service without a clear confirmation step.

Mitigation: Ask the user to confirm the city before requesting weather data, and narrow activation to clearly weather-related requests.

## Reference(s):

- [wttr.in JSON weather endpoint](https://wttr.in/{城市}?format=j1)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown-style Chinese text response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include weather description, temperature, feels-like temperature, humidity, wind, UV index, air quality when available, practical advice, and solar-term context.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
