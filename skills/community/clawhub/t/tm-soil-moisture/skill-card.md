## Description:

TM Soil Moisture Skill helps agents query local multi-depth soil temperature and moisture sensor data, aggregate field conditions, and provide irrigation decision support for Shiny-leaved yellowhorn planting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lu87985](https://clawhub.ai/user/lu87985)

### License/Terms of Use:

MIT-0

## Use Case:

Farm operators, agricultural advisors, and external developers use this skill to inspect device-level soil profiles, compare moisture and temperature across field depths, and receive irrigation guidance from local sensor records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Irrigation recommendations may be misleading if local database values are stale, malformed, or unvalidated, and weather is simulated.

Mitigation: Treat the skill as decision support only; verify sensor freshness and field conditions before taking irrigation action.

Risk: The skill depends on local database access and the MCP dependency in the host environment.

Mitigation: Install it in an isolated environment, pin the MCP dependency, and connect it only to the intended agriculture database.

## Reference(s):

- [Skill README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/lu87985/skills/tm-soil-moisture)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown-formatted text with sensor readings, aggregate statistics, alerts, and irrigation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include soil temperature in degrees Celsius, moisture percentages, device health indicators, and decision-support guidance based on local database records.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
