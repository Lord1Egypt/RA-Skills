## Description:

Predicts peak, dip, and second-peak work windows from self-reported sleep using WhenPeak's API, then turns the result into scheduling advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whenpeak](https://clawhub.ai/user/whenpeak)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to choose times for meetings, interviews, exams, presentations, deep-work blocks, and daily plans based on predicted cognitive performance from sleep. It also helps agents explain timing tradeoffs, avoid unsupported multi-night planning, and offer optional single-day performance charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided sleep, wake, exercise, and fragmentation details to an external WhenPeak API.

Mitigation: Tell the user before the first API call what sleep data will be sent and skip the API call if they do not want to share it.

Risk: The remote API influences user-facing scheduling recommendations and may prompt users to share more health data.

Mitigation: Treat wearable, Apple Health, or additional sleep-history sharing as optional and explain that it means sharing more health data with WhenPeak.

Risk: Self-reported single-night data has limited confidence for future dates, body-clock shifts, or multi-night event preparation.

Mitigation: Avoid unsupported multi-night plans, clearly state when projections repeat a baseline forward, and frame predictions as scheduling guidance rather than guaranteed outcomes.

## Reference(s):

- [WhenPeak homepage](https://whenpeak.com)
- [WhenPeak documentation](https://whenpeak.com/docs)
- [ClawHub skill page](https://clawhub.ai/whenpeak/skills/whenpeak)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown scheduling advice with optional JSON-backed PNG chart output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public WhenPeak API responses; optional charting is single-day only.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
