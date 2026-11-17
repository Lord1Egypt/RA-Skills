## Description:

Retrieves YZL-AIoT device and sensor data and sends remote device-control commands through the YZL Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzlkj](https://clawhub.ai/user/yzlkj)

### License/Terms of Use:

MIT-0

## Use Case:

Device operators and developers use the skill to check sensor readings and device history or send commands to authorized YZL-AIoT devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Valve or switch commands can change physical devices without a separate confirmation step.

Mitigation: Require explicit user confirmation before each control command and use only an authorized YZLIOT_API_KEY.

Risk: The bundled repository-sync script can stage and push local files using developer tokens.

Mitigation: Do not run sync.sh unless publishing is intended; first review every file that would be staged and pushed.

## Reference(s):

- [YZL Open API documentation](https://cn6l1w4yn0.apifox.cn)
- [YZL-AIoT ClawHub release](https://clawhub.ai/yzlkj/skills/yzl-aiot)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text device readings and command status, with API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and an authorized YZLIOT_API_KEY.]

## Skill Version(s):

1.2.1 (source: server release metadata, artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
