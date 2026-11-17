## Description:

Get current weather and forecasts from wttr.in without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[164149043](https://clawhub.ai/user/164149043)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to provide shell-command guidance for retrieving current conditions, forecasts, compact weather summaries, and custom weather formats from wttr.in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups send location names, format parameters, and request metadata to wttr.in.

Mitigation: Avoid sensitive private location labels and review commands before execution.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [Weather Tools on ClawHub](https://clawhub.ai/164149043/skills/weather-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands call wttr.in and may include location names or output format parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
