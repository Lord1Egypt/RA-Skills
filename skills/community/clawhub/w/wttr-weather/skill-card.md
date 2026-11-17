## Description:

Helps agents retrieve current weather, forecasts, and moon phases from wttr.in in text, structured data, and image formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fbbyqsyea](https://clawhub.ai/user/fbbyqsyea)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can look up weather for cities and other locations, compare forecasts, check moon phases, and obtain weather data or images for reports and integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented bash-function example executes code downloaded from wttr.in.

Mitigation: Inspect and trust the downloaded code before running it; prefer the bundled CLI for routine queries.

Risk: Weather requests can disclose a queried location or expose the requester's IP address to an external service.

Mitigation: Use explicit city-level locations instead of GPS or IP-based lookups, and limit the service URL to wttr.in or wttr.is.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fbbyqsyea/skills/wttr-weather)
- [wttr.in usage help](https://wttr.in/:help)
- [Weather quick reference](artifact/references/quick-reference.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance, Files]

**Output Format:** [Plain text or Markdown guidance; optional weather JSON, metrics text, and PNG images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Location, language, units, and view are configurable; live queries contact wttr.in or wttr.is.]

## Skill Version(s):

2.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
