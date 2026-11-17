## Description:

Weather and forecasts with no API key, using one wttr.in fetch by default and Open-Meteo only as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maximedogawa](https://clawhub.ai/user/maximedogawa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer current weather and forecast questions for named places. It favors concise, plain-language forecast summaries and falls back to Open-Meteo when wttr.in is unavailable or structured JSON is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location names entered by users are sent to public weather services.

Mitigation: Avoid using sensitive or private location descriptions, and disclose that wttr.in and Open-Meteo may receive requested place names.

Risk: Some wttr.in examples use plaintext host syntax that could be executed over HTTP by default.

Mitigation: Prefer HTTPS URLs for wttr.in requests when running curl or fetch commands.

## Reference(s):

- [Weather 2.0 on ClawHub](https://clawhub.ai/maximedogawa/skills/weather-2-0)
- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo weather API documentation](https://open-meteo.com/en/docs#api_form)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise Markdown or plain text with optional inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should avoid coordinates and WMO codes unless the user asks for technical detail.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
