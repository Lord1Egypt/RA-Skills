## Description:

Add HTTP OTA (Over-The-Air) firmware update capability to Unihiker K10 Arduino projects, including AP/STA projects and ESP-NOW projects that need a safe OTA maintenance mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockets-cn](https://clawhub.ai/user/rockets-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add and maintain HTTP OTA firmware updates for Unihiker K10 Arduino projects, including AP/STA setups and ESP-NOW projects that need a temporary OTA maintenance mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OTA pattern can expose an unauthenticated HTTP firmware update endpoint to anyone with network access.

Mitigation: Add per-device authentication, keep OTA mode temporary and locally triggered, and use signed firmware or an equivalent integrity check before using it on a real network.

Risk: Shared default access point credentials can make OTA maintenance mode easier to reach than intended.

Mitigation: Avoid shared default AP passwords and provision unique device credentials.

Risk: Changing the K10 partition table can erase local data or damage built-in AI model regions if offsets are wrong.

Mitigation: Review the partition table before the first USB flash and keep OTA application partitions from overlapping the model, voice_data, and fr regions.

## Reference(s):

- [K10 HTTP OTA Implementation Guide](references/ota-implementation.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code, command examples, and helper upload scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Python and PowerShell helper upload scripts.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
