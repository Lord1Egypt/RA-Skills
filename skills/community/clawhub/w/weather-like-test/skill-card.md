## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[guxiaolong01](https://clawhub.ai/user/guxiaolong01)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to get quick current weather summaries and forecasts from public weather services without configuring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups can expose sensitive location information when exact home or work locations are used.

Mitigation: Use coarse locations such as a city, region, or airport code rather than exact private coordinates.

Risk: Plain host examples for wttr.in may rely on implicit transport behavior.

Mitigation: Prefer explicit https:// wttr.in URLs, especially on untrusted networks.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast endpoint](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)
- [ClawHub skill page](https://clawhub.ai/guxiaolong01/skills/weather-like-test)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and weather-service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the documented command examples; no API key is required.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
