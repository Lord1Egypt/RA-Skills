## Description:

Get current weather and forecasts with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happyzengfen](https://clawhub.ai/user/happyzengfen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for quick weather lookup commands, compact forecasts, full forecasts, PNG weather output, or JSON weather data without configuring API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Typed locations, airport codes, or coordinates may be sent to public weather APIs when the examples are run.

Mitigation: Avoid querying sensitive private locations, use coarse locations where practical, and review commands before execution.

Risk: Weather results depend on third-party public services and may be unavailable, delayed, or inaccurate.

Mitigation: Use the Open-Meteo fallback when wttr.in is unavailable and verify important weather-dependent decisions against an authoritative source.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast API example](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)
- [ClawHub skill page](https://clawhub.ai/happyzengfen/skills/weather-test-1774063891)
- [Publisher profile](https://clawhub.ai/user/happyzengfen)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown with inline bash code blocks and API output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; weather lookups call public wttr.in or Open-Meteo endpoints and may produce text, JSON, or PNG output.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
