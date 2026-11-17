## Description:

Provides global city weather forecasts using the free wttr.in API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickcen](https://clawhub.ai/user/nickcen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to request weather forecasts for global cities by name, choose Celsius or Fahrenheit output, and optionally receive detailed or JSON-formatted results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location names are sent to wttr.in when forecasts are requested.

Mitigation: Avoid submitting sensitive private locations and review external data-sharing expectations before use.

Risk: The documented setup installs curl and jq system packages.

Mitigation: Install dependencies only in approved environments and review package-manager commands before execution.

Risk: The artifact documentation is Chinese-only.

Mitigation: Confirm command options and dependency requirements before delegating the skill to users who do not read Chinese.

## Reference(s):

- [ClawHub Weather Cli Skill Page](https://clawhub.ai/nickcen/skills/weather-cli)
- [wttr.in Weather Service](https://wttr.in)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional plain-text or JSON weather output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for weather requests and jq for JSON mode; location queries are sent to wttr.in.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
