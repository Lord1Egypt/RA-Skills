## Description:

Get current weather conditions and forecasts for named locations via wttr.in or Open-Meteo without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaojie66](https://clawhub.ai/user/shaojie66)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to answer current weather, rain, temperature, and forecast questions for a named city, region, or airport code. It supports quick travel-planning weather checks but excludes historical weather, severe alerts, climate analysis, and specialized aviation or marine forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookup commands may use non-HTTPS wttr.in URLs in examples.

Mitigation: Prefer https://wttr.in URLs when adapting or executing commands.

Risk: Simple weather lookups may be inappropriate for severe weather, aviation, marine, or other safety-critical decisions.

Mitigation: Use official alerting sources or specialized weather services for those decisions.

Risk: Public weather services may rate limit repeated requests.

Mitigation: Throttle or cache repeated lookups instead of issuing high-volume curl requests.

## Reference(s):

- [wttr.in Help](https://wttr.in/:help)
- [ClawHub Skill Page](https://clawhub.ai/shaojie66/skills/shaojie66-weather)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, text weather summaries, and optional JSON or PNG weather outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl. No API key is required. Prefer HTTPS wttr.in URLs and avoid use for safety-critical weather decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
