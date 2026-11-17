## Description:

Gets current WeatherFlow Tempest station observations and day, month, or year station statistics through the Tempest REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wranglerdriver](https://clawhub.ai/user/wranglerdriver)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve backyard or home weather observations and historical station summaries from their own WeatherFlow Tempest station or device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a Tempest API token and station or device IDs.

Mitigation: Configure TEMPEST_API_TOKEN and IDs through the environment, and avoid passing the token on the command line when possible.

Risk: Private configuration files or keys could be accidentally included when packaging the skill.

Mitigation: Check the skill directory before packaging and keep .env files and private keys outside the artifact.

## Reference(s):

- [Tempest API Notes](references/tempest-api.md)
- [Tempest Weather project homepage](https://github.com/wranglerdriver/tempest-weather)
- [Tempest platform](https://tempest.earth)
- [WeatherFlow Tempest REST API base](https://swd.weatherflow.com/swd/rest)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON plus an optional concise human-readable weather summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tempest API token and station or device ID; supports US or metric units and day, month, or year historical stats.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
