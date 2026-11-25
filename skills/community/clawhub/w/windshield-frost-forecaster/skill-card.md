## Description:

Use on cold evenings to predict whether frost will form on your car windshield or home windows tonight: dew-point + radiative-cooling physics (clear sky, wind, humidity), parking-duration verdicts for uncovered vs covered, morning scrape-time penalty, and cover/defrost tactics by frost class.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Drivers and homeowners use the skill with evening weather inputs to estimate whether exposed glass may frost, decide whether to cover it, and plan suitable morning defrosting. It also provides estimates for shorter outdoor parking periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Frost estimates can be inaccurate because they rely on a simplified model and forecast inputs.

Mitigation: Check a current local forecast and treat the result as a planning estimate; confirm conditions before relying on it.

## Reference(s):

- [Frost Physics Behind the Windshield Frost Forecaster](references/frost-physics.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/windshield-frost-forecaster)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain-text frost verdict and parking-duration table, with optional JSON output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses overnight minimum temperature, dew point or relative humidity, wind speed, cloud cover, and optional parking duration as inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
