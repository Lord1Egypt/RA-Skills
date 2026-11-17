## Description:

Control SwitchBot smart home devices (curtains, plugs, lights, locks, etc.) via SwitchBot Cloud API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home operators use this skill to configure SwitchBot Cloud API credentials, discover devices, and control or inspect supported SwitchBot devices such as curtains, plugs, lights, locks, humidifiers, and meters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue broad physical-device commands, including lock, unlock, plug, lighting, curtain, humidifier, and raw device commands.

Mitigation: Review each requested device action before execution, and require explicit confirmation for unlock, power, batch, and raw command operations.

Risk: Durable SwitchBot API credentials enable ongoing access to real smart-home devices.

Mitigation: Store credentials with restrictive file permissions, avoid displaying token or secret values, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub Switchbot skill page](https://clawhub.ai/daaab/skills/switchbot)
- [SwitchBot Cloud API v1.1 endpoint](https://api.switch-bot.com/v1.1)
- [Publisher profile](https://clawhub.ai/user/daaab)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SwitchBot credentials and may trigger SwitchBot Cloud API actions against physical devices.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
