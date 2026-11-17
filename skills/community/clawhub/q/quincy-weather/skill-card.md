## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for current weather, compact forecasts, or weather API examples without needing an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups contact third-party services and disclose the queried location.

Mitigation: Use the skill only with locations that are acceptable to share with wttr.in or Open-Meteo.

Risk: Some wttr.in examples omit an explicit HTTPS scheme.

Mitigation: Prefer explicit https:// URLs when adapting or executing the examples.

Risk: The PNG example writes to /tmp/weather.png and could overwrite an existing temporary file.

Mitigation: Choose a unique output path before saving PNG weather output.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)
- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/quincy-weather)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and weather service URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON when using the Open-Meteo fallback example; requires curl for command examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
