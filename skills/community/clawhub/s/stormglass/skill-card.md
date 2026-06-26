## Description: <br>
Fetches surf-relevant ocean conditions from Stormglass by spot name or coordinates, including current snapshots and 1-3 day forecast windows with tides, gusts, and water temperature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgorissen](https://clawhub.ai/user/dgorissen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current and forecast surf conditions for a beach or surf spot, then feed the stable JSON into cron jobs, downstream summaries, or surf-window analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Surf spot names or coordinates are sent to Stormglass and may be sent to Google or OpenStreetMap when location lookup is used. <br>
Mitigation: Use direct coordinates or mock mode for privacy-sensitive workflows, and install only when this data sharing is acceptable. <br>
Risk: The optional Google geocoding API key can be exposed in error output or cron logs. <br>
Mitigation: Store API keys in environment-backed secrets and avoid the Google geocoding path in cron logs until URL and key redaction is confirmed. <br>


## Reference(s): <br>
- [Stormglass API documentation](https://docs.stormglass.io/#/) <br>
- [Project homepage](https://github.com/dgorissen/stormglass-skill) <br>
- [Skill reference](reference.md) <br>
- [Skill examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON or human-readable terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stable top-level JSON keys include meta, location, now, forecast, and tides; unavailable metrics are represented as null.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
