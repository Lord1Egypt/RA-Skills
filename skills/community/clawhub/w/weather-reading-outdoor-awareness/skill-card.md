## Description:

Practical weather observation and environmental awareness guidance for people working outdoors, making weather-dependent decisions without phone access, or developing environmental situational awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

Outdoor workers, hikers, planners, and other external users use this skill to interpret clouds, wind, pressure, lightning, heat, cold, and cancellation thresholds when phone or forecast access is limited.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests filesystem access even though server security says the documented function does not use or scope it.

Mitigation: Review before installing, prefer a version without filesystem access or with a clearly scoped permission requirement, and install through a pinned or trusted ClawHub CLI path.

Risk: Incorrect or overconfident weather-safety guidance could lead to unsafe outdoor decisions.

Mitigation: Use the skill as advisory support, verify conditions with official alerts or forecasts when available, and prioritize emergency services or shelter guidance for lightning, heat stroke, hypothermia, and severe weather.

## Reference(s):

- [National Weather Service](https://www.weather.gov)
- [NOAA](https://www.noaa.gov)
- [Wilderness Medical Society](https://wms.org)
- [Anthropic - Labor market impacts of AI](https://www.anthropic.com/research/labor-market-impacts)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with concise safety thresholds and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include localized units and region-specific severe weather alert references when user location is known.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
