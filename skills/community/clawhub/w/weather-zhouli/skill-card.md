## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current weather and forecasts for cities, airport codes, or coordinates using public weather services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups send the requested location to public weather services.

Mitigation: Avoid submitting highly sensitive precise locations when that privacy boundary matters.

Risk: Some wttr.in examples use hostnames without an explicit scheme.

Mitigation: Use explicit HTTPS URLs for wttr.in requests when deploying or documenting the skill.

Risk: Weather data and external service responses may be unavailable or inaccurate.

Mitigation: Treat returned forecasts as public weather-service output and use the Open-Meteo fallback when the primary service is unsuitable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/weather-zhouli)
- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compact text forecasts, full terminal forecasts, API JSON examples, or PNG retrieval commands.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
