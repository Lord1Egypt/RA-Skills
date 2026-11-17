## Description:

Automates sunsetbot.top lookups with agent-browser to return a requested city and date's sunset vividness, aerosol (AOD), and a short sunset probability assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiwei106](https://clawhub.ai/user/weiwei106)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to check sunset or sunset-glow conditions for a city and optional date, then receive the vividness, aerosol level, and a plain-language probability assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City and date inputs are submitted to sunsetbot.top through browser automation.

Mitigation: Avoid using the skill for sensitive location queries when disclosure of that city/date would be a concern.

Risk: Sunset vividness and aerosol values are forecasts from an external website and may be unavailable, delayed, or inaccurate.

Mitigation: Treat results as planning guidance and verify important decisions with the source site or another forecast service.

## Reference(s):

- [sunsetbot detailed forecast page](https://sunsetbot.top/detailed/)
- [ClawHub skill page](https://clawhub.ai/weiwei106/skills/sunsetbot-watch)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style text with date, vividness, aerosol, and conclusion fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser automation to query sunsetbot.top; no local files, scripts, credentials, or persistence are included.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
