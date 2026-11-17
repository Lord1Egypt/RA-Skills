## Description:

Fetches coordinate-based weather forecasts from MET Norway's yr.no Locationforecast API, including current conditions and tomorrow forecast summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandon2255p](https://clawhub.ai/user/brandon2255p)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, and developers use this skill when an agent needs current weather conditions or forecast summaries for a user-supplied latitude and longitude.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented unpinned Git-based pip install can execute mutable external code.

Mitigation: Install only from a reviewed commit hash or verified release artifact that matches the expected source.

Risk: Latitude, longitude, and optional altitude are sent to MET Norway when forecasts are fetched.

Mitigation: Use coordinates only when sharing that location data with MET Norway is acceptable for the user and deployment context.

## Reference(s):

- [ClawHub Yr Weather Skill Page](https://clawhub.ai/brandon2255p/skills/yr-weather)
- [MET Norway Locationforecast API endpoint](https://api.met.no/weatherapi/locationforecast/2.0/compact)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text weather summaries and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires latitude and longitude; optional altitude is passed to MET Norway.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact package version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
