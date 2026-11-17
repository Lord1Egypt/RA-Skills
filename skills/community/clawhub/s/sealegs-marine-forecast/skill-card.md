## Description:

Get AI-powered marine weather forecasts for any location worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sealegs-ai-coder](https://clawhub.ai/user/sealegs-ai-coder)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and marine operators use this skill to request SeaLegs SpotCast forecasts for specific coordinates, dates, vessels, and trip details. The skill helps agents present wind, wave, visibility, precipitation, and GO/CAUTION/NO-GO safety classifications from the SeaLegs API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Python workflow can send SEALEGS_API_KEY to an API base URL supplied through the environment.

Mitigation: Leave SEALEGS_API_BASE_URL unset for normal use, or set it only to a destination you fully trust.

Risk: The API key may be exposed if stored in shared .env files or copied into shared configuration.

Mitigation: Store SEALEGS_API_KEY in a private environment or secret manager and avoid committing or sharing local credential files.

Risk: Forecast metadata and webhook-bound fields may contain sensitive trip or personal details.

Mitigation: Keep metadata minimal and avoid personal, private, or sensitive operational details in API requests and webhook payloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sealegs-ai-coder/skills/sealegs-marine-forecast)
- [SeaLegs Developer Portal](https://developer.sealegs.ai)
- [SeaLegs API Documentation](https://developer.sealegs.ai/docs/)
- [SpotCast Workflow Example](artifact/spotcast-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SEALEGS_API_KEY and curl; the included workflow may poll asynchronous forecast endpoints before presenting results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
