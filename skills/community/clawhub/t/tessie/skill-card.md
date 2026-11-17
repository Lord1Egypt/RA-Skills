## Description:

Control and monitor Tesla vehicles through the Tessie API for battery, climate, charging, drives, location, and vehicle state management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baanish](https://clawhub.ai/user/baanish)

### License/Terms of Use:


## Use Case:

Tesla owners with Tessie accounts use this skill to ask an agent to check vehicle telemetry and manage common vehicle workflows such as climate, charging, location, drive history, vehicle status, and FSD statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Tessie account and vehicle telemetry, including location-related data.

Mitigation: Install only for trusted agent contexts, limit access to the vehicle owner, and avoid sharing telemetry output unless it has been reviewed.

Risk: The skill can issue real vehicle-control commands.

Mitigation: Review commands before execution and avoid shared or fully automated contexts for actions that affect the vehicle.

Risk: A custom TESSIE_API_URL endpoint can expose the Tessie bearer key.

Mitigation: Use the default Tessie API endpoint unless the alternative endpoint is fully trusted, and prefer the narrowest available Tessie API key permissions.

## Reference(s):

- [Tessie Skill Listing](https://clawhub.ai/baanish/skills/tessie)
- [Tessie Developer Portal](https://tessie.com/developers)
- [Tessie API Documentation](https://developer.tessie.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Plain text command output with shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tessie API key and may read vehicle telemetry or issue vehicle-control requests.]

## Skill Version(s):

2.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
