## Description:

Get current weather and forecasts. Use when user needs to check current weather, get forecast for travel planning, or monitor weather conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current weather conditions and short multi-day forecasts for named locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups disable HTTPS certificate and hostname verification, so responses should be treated as untrusted until the implementation is fixed.

Mitigation: Use the skill only for low-stakes weather checks, review results before acting on them, and restore normal HTTPS verification before relying on it in production workflows.

Risk: Location names entered by users are sent to the external wttr.in service.

Mitigation: Avoid submitting sensitive or precise personal locations unless that disclosure is acceptable for the deployment context.

Risk: Weather results may be unsuitable for safety-critical travel, emergency, or automated decisions.

Mitigation: Confirm important forecasts with an authoritative weather source before making consequential decisions.

## Reference(s):

- [wttr.in weather service](https://wttr.in)
- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/weather-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text or JSON command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast range is documented as 1-7 days; location names are sent to wttr.in.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
