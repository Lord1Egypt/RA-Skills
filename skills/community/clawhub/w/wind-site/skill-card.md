## Description:

Wind rose, wind speed/direction at a site; supports site and urban wind assessment (data only; detailed CFD is out of scope).

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrost](https://clawhub.ai/user/qrost)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, architects, and site analysts use this skill to fetch current or recent wind speed and direction for coordinates and generate wind rose images for site wind context. It supports early site and urban wind assessment inputs, while detailed CFD and pedestrian comfort simulation remain out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requested coordinates and date ranges to Open-Meteo to fetch wind data.

Mitigation: Install and use it only when sharing those location and time-range inputs with Open-Meteo is acceptable.

Risk: Python dependencies may vary across environments if installed without version pins.

Mitigation: Use a virtual environment or other isolation and prefer pinned dependency versions for reproducible installs.

Risk: Wind rose and wind speed outputs are climate context only and do not model building-level or pedestrian wind effects.

Mitigation: Use CFD, wind-tunnel studies, or specialist tools for detailed urban wind and comfort assessment.

## Reference(s):

- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Open-Meteo Historical API](https://archive-api.open-meteo.com/v1/archive)
- [ClawHub Skill Page](https://clawhub.ai/qrost/skills/wind-site)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown summary with command output and optional PNG wind rose image]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on latitude, longitude, optional date range, and optional image output path.]

## Skill Version(s):

1.1.1 (source: frontmatter, clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
