## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lei335](https://clawhub.ai/user/lei335)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to get curl-based guidance for retrieving current weather and forecasts from public weather services without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups can send requested locations or coordinates to third-party public weather services.

Mitigation: Avoid querying locations that are sensitive, and review generated curl commands before execution.

Risk: Weather responses from public services may be unavailable, stale, or formatted differently than expected.

Mitigation: Cross-check important weather decisions with an authoritative weather source and handle fallback JSON responses explicitly.

## Reference(s):

- [wttr.in Help](https://wttr.in/:help)
- [Open-Meteo Forecast API Documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; no API key is required by the documented services.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
