## Description:

Helps agents provide command-line weather queries and forecasts using wttr.in or Open-Meteo without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external users can use this skill when an agent needs to suggest terminal weather queries, quick forecasts, custom wttr.in formats, or Open-Meteo JSON calls for scripting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries contact external weather services and may disclose requested cities, airport codes, or coordinates.

Mitigation: Avoid sending sensitive locations and review generated curl commands before execution.

Risk: The source instructions are primarily Chinese, which may reduce clarity for non-Chinese users.

Mitigation: Review the command intent and service documentation before adapting the examples.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-weather)
- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather calls contact external services and may disclose requested locations or coordinates.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
