## Description:

Helps an agent answer weather requests for a specified city by gathering public weather information and returning temperature, conditions, humidity, wind, and a brief practical tip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyifei](https://clawhub.ai/user/gyifei)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer city-specific weather questions. It extracts the city and requested time, fetches public weather information, formats the core conditions, and asks a follow-up question when the city is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather information fetched from public webpages may be incomplete, stale, or vary by source.

Mitigation: Prefer current, reputable weather sources and include the requested city and time in the response so users can spot mismatches.

Risk: The artifact is written in Chinese and may answer in Chinese even when a user expects another language.

Mitigation: Adapt the response language to the user's preference when deploying in multilingual environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gyifei/skills/weather-query-ll)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text weather summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes city and time, temperature in Celsius by default, weather condition, humidity, wind, and a short weather tip.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
