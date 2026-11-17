## Description:

Multi-model ensemble weather forecasts comparing GFS, ECMWF, JMA, GEM, ICON, ARPEGE, GraphCast and more. Get high temperature predictions from up to 9 independent weather models with agreement analysis for 16 global cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasnocodo](https://clawhub.ai/user/lucasnocodo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, weather enthusiasts, event planners, travelers, and researchers use this skill to request multi-model high-temperature forecasts, compare model agreement, and review ensemble uncertainty for supported global cities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be sent to a configurable Weather Ensemble API host if WEATHER_ENSEMBLE_HOST is set.

Mitigation: Use only the default HTTPS service unless a replacement host is trusted, and treat WEATHER_ENSEMBLE_API_KEY as a credential.

Risk: The server-side API trust boundary is not fully documented in the release evidence, and the authoritative security verdict is suspicious.

Mitigation: Review the service trust boundary before installation and prefer a future version that pins or validates the HTTPS host before sending credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucasnocodo/skills/weather-ensemble-forecast)
- [Weather Ensemble API forecast endpoint](https://polymarket-scanner.fly.dev/forecast/{city})
- [Weather Ensemble API cities endpoint](https://polymarket-scanner.fly.dev/cities)
- [Weather Ensemble API key request endpoint](https://polymarket-scanner.fly.dev/keys/free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with JSON data returned by shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq. Optional WEATHER_ENSEMBLE_API_KEY extends access; WEATHER_ENSEMBLE_HOST should remain unset unless the service is trusted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
