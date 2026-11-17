## Description:

Fetches live weather data from a WeatherFlow Tempest weather station and returns structured JSON with current conditions, wind, precipitation, and lightning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mogglemoss](https://clawhub.ai/user/mogglemoss)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve current conditions from their configured WeatherFlow Tempest station, including wind, precipitation, lightning, solar, and basic station status data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal Tempest tokens can appear in request URLs, shell history, or logs.

Mitigation: Prefer environment variables, avoid command-line token flags where possible, and redact token-bearing URLs from logs and shared transcripts.

Risk: Station observations may reveal precise or sensitive location details.

Mitigation: Review the configured station before installation, avoid using home or sensitive stations when unnecessary, and limit sharing of station metadata.

Risk: Broad weather questions may cause an agent to use the configured personal station data.

Mitigation: Make the configured station scope clear to users and confirm before using it in sensitive contexts.

## Reference(s):

- [Tempest REST API Documentation](https://weatherflow.github.io/Tempest/api/)
- [Tempest Observation Field Reference](references/obs_fields.md)
- [Tempest Weather Skill on ClawHub](https://clawhub.ai/mogglemoss/skills/tempest-weather-wf)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live station observations from the Tempest REST API using user-provided credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
