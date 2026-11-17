## Description:

Access Apple WeatherKit REST API for detailed weather forecasts using JWT authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmcq](https://clawhub.ai/user/jimmcq)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch current weather and daily forecasts for specified coordinates and date ranges through Apple WeatherKit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise coordinates and full WeatherKit responses may be written to logs.

Mitigation: Remove debug logging or make it opt-in with redaction before use in shared, hosted, CI, or centrally logged environments.

Risk: The skill depends on Apple Developer identifiers and a WeatherKit private key file.

Mitigation: Store credentials in a secret manager or protected environment variables, restrict private key file permissions, and avoid committing key material.

## Reference(s):

- [Apple WeatherKit REST API Documentation](https://developer.apple.com/documentation/weatherkitrestapi/)
- [WeatherKit Skill on ClawHub](https://clawhub.ai/jimmcq/skills/weatherkit)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON forecast payloads printed to stdout, with operational errors and debug details printed to stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Apple WeatherKit credentials in environment variables and latitude/longitude inputs for location-specific forecasts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
