## Description:

Provides a unified interface for agents to issue smart-home commands to Home Assistant, Xiaomi Mijia, and Tuya devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home automation builders use this skill to let an agent translate intents into constrained CLI calls for lighting, HVAC, locks, alarms, and feeders across supported integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact physical actions involving locks, feeders, HVAC, and other smart-home devices.

Mitigation: Use dry-run by default and require explicit human confirmation before enabling real actuation for locks, feeders, and HVAC.

Risk: Network credentials and device endpoints are sensitive and can increase exposure if over-privileged or transmitted insecurely.

Mitigation: Use least-privileged environment-injected credentials, avoid HTTP Home Assistant endpoints, and rotate secrets used for Home Assistant, Mijia, and Tuya integrations.

Risk: Device-specific command values may produce unsafe or unintended behavior if mappings and limits are wrong.

Mitigation: Verify each device mapping and value limit before setting S2_ENABLE_REAL_ACTUATION=True.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-spatial-adapters)
- [Publisher profile](https://clawhub.ai/user/spacesq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run unless S2_ENABLE_REAL_ACTUATION is enabled; real actuation depends on configured device endpoints and credentials.]

## Skill Version(s):

2.0.7 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
