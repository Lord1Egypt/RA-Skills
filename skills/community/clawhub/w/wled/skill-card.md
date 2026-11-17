## Description:

Control WLED LED controllers via HTTP API. Use when a user asks to control WLED lights, LED strips, or ESP-based LED controllers. Supports power on/off, brightness, colors (RGB), effects, palettes, presets, and device status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rowbotik](https://clawhub.ai/user/rowbotik)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation users use this skill to control WLED LED strips, matrices, and ESP-based controllers from an agent workflow. It supports direct device operations such as power, brightness, RGB color, effects, palettes, presets, status checks, and host alias configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can immediately change the selected WLED controller's light state.

Mitigation: Verify the target host, environment variable, or saved alias before running power, brightness, color, effect, palette, or preset commands.

Risk: A stale address or alias can point commands at the wrong light controller.

Mitigation: Use stable hostnames or reserved/static IP addresses and keep saved WLED aliases current.

## Reference(s):

- [WLED HTTP API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/rowbotik/skills/wled)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send HTTP commands that change the selected WLED device state when executed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
