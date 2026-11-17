## Description:

Display a time dashboard with a live countdown to the 2026 summer solstice, Beijing sunrise and sunset times, and current time information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a live HTML time widget for summer solstice countdowns and Beijing-specific sunrise, sunset, solar noon, day length, date, and clock displays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated widgets contact public time and sunrise APIs when opened.

Mitigation: Review deployment policy for browser access to those public APIs before using or sharing the widget.

Risk: The sunrise panel is intentionally Beijing-specific and may be mistaken for the user's local sunrise and sunset data.

Mitigation: Label the panel as Beijing, China and adjust coordinates only when a different location is intended.

## Reference(s):

- [Skill page](https://clawhub.ai/goog/skills/summer)
- [USNO seasons API](https://aa.usno.navy.mil/api/seasons?year=2026)
- [Sunrise-sunset API for Beijing](https://api.sunrise-sunset.org/json?lat=39.9075&lng=116.3972&formatted=0&date=today)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML may fetch public solstice and sunrise/sunset APIs at runtime.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
