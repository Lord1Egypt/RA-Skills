## Description:

Generates Volcengine RTC-bound device-control JSON commands for actions such as pan, volume, brightness, power-off, emoji display, and device vibration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huang-zhibin](https://clawhub.ai/user/huang-zhibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to translate natural-language device-control requests into structured Volcengine RTC `send_command` JSON for currently bound hardware devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Natural-language intent can become an immediate hardware shutdown command, including `power_off` with zero delay.

Mitigation: Require explicit user confirmation before shutdown or similarly disruptive device-control commands, especially for important or shared devices.

Risk: Device-control commands affect bound hardware through the RTC signaling path.

Mitigation: Use only authenticated sessions for the current logged-in user, keep audit logs enabled, and restrict command transport to the documented Volcengine RTC endpoint.

## Reference(s):

- [Protocol Specification](references/protocol.md)
- [Volcengine RTC signaling endpoint](https://rtc.volcengine.com)
- [ClawHub skill page](https://clawhub.ai/huang-zhibin/skills/volcengine-rtc-device-control)

## Skill Output:

**Output Type(s):** [JSON, Configuration, Guidance]

**Output Format:** [JSON command objects with brief guidance when a requested control is unsupported]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the `send_command` name and a `parameters` object containing `command_name` plus optional action parameters such as angle, speed, level, step, or delay.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
