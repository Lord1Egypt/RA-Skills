## Description:

Get current weather and forecasts (no API key required).

This skill is ready for commercial/non-commercial use.

## Publisher:

[erhwenkuo](https://clawhub.ai/user/erhwenkuo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for current weather or forecast lookup commands using public wttr.in or Open-Meteo services without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookup queries are sent to public weather services and may reveal the queried location.

Mitigation: Use only the location detail needed for the forecast, such as a city or airport code, and avoid sensitive personal addresses.

Risk: The skill depends on external weather services being reachable and returning usable responses.

Mitigation: Use Open-Meteo as a fallback when wttr.in is unavailable or unsuitable for programmatic JSON output.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and API URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command examples; no API key required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
