## Description:

Generate daily Weather Intelligence Digest using NOAA/NWS data with customizable locations and alert monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyboy1241](https://clawhub.ai/user/dannyboy1241)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to generate daily weather briefings for configured locations, including forecast highlights and active alert summaries from NOAA/NWS public APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional HTML reports may include unescaped weather or configuration text that could run as active content if opened, hosted, or published.

Mitigation: Review or fix HTML escaping before sharing generated HTML; prefer Markdown or JSON output when publishing without additional sanitization.

Risk: Dependencies are not pinned to exact versions.

Mitigation: Install in a virtual environment and pin reviewed dependency versions for repeatable deployments.

## Reference(s):

- [Weather.gov API](https://api.weather.gov)
- [ClawHub skill page](https://clawhub.ai/dannyboy1241/skills/weather-intelligence-digest-fresh)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration]

**Output Format:** [Markdown, optional HTML, optional JSON, and setup or usage commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and pip; uses a JSON configuration file with location names and latitude/longitude pairs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
