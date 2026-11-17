## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[clearlovetop7](https://clawhub.ai/user/clearlovetop7)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to fetch current weather, compact forecasts, and programmatic weather JSON for a requested city, airport code, or coordinate pair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups may disclose the requested city, airport code, or coordinates to wttr.in or Open-Meteo.

Mitigation: Avoid sending sensitive or unnecessary precise locations; prefer coarse city or airport-code queries when exact coordinates are not required.

Risk: Public weather service responses can be unavailable, stale, or formatted differently than expected.

Mitigation: Use Open-Meteo as a fallback for programmatic JSON and verify weather-sensitive decisions against an authoritative source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clearlovetop7/skills/weatherclear)
- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return text, PNG image files, or JSON depending on the selected weather endpoint and curl options.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
