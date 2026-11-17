## Description:

Generates SVG weather and outfit recommendation posters for Wuhan by default or a user-specified city.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ll21121](https://clawhub.ai/user/ll21121)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to create localized weather posters that combine current weather details with outfit recommendations and save the result as an SVG file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact an external weather source to obtain current conditions.

Mitigation: Use it only where external weather lookups are acceptable, or provide weather data through an approved local or agent-available source.

Risk: The skill writes an SVG file named for the requested city into the workspace.

Mitigation: Review the output filename and destination before use when the workspace has naming or file-placement requirements.

## Reference(s):

- [Weather Poster SVG Template](artifact/references/TEMPLATE.md)
- [ClawHub skill page](https://clawhub.ai/ll21121/skills/weather-poster)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [SVG file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves output as {city}-weather-poster.svg in the workspace.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
