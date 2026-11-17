## Description:

Monitor solar weather conditions including geomagnetic storms, solar flares, aurora forecasts, and solar wind data using NOAA Space Weather Prediction Center real-time data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:


## Use Case:

External users such as ham radio operators, aurora watchers, satellite operators, power-grid operators, and space-weather enthusiasts use this skill to check current and forecast NOAA SWPC space-weather conditions, alerts, solar wind, and aurora outlooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live read-only network requests to NOAA SWPC for space-weather data.

Mitigation: Use it only in environments where outbound access to NOAA SWPC is permitted and expected.

Risk: Current conditions, forecasts, alerts, and aurora outlooks depend on external data availability and freshness.

Mitigation: Check timestamps in the output and treat network or API failures as unavailable data rather than quiet space-weather conditions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/capt-marbles/skills/solar-weather)
- [NOAA Space Weather Prediction Center](https://www.swpc.noaa.gov/)
- [NOAA SWPC services endpoint](https://services.swpc.noaa.gov)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text command output or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from live read-only NOAA SWPC data requests and may reflect current network or API availability.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
