## Description:

Controls Raspberry Pi servos with hardware PWM when precise servo control is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cld1994](https://clawhub.ai/user/cld1994)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hardware makers use this skill to configure Raspberry Pi hardware PWM, install the rpi-hardware-pwm Python library, and troubleshoot servo control on GPIO/PWM channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged hardware and boot-configuration changes can alter PWM, audio, or startup behavior on the Raspberry Pi.

Mitigation: Review commands before use, back up boot configuration, and obtain user approval before changing configuration or rebooting.

Risk: Servo pulse-width settings and the sample infinite loop can move hardware unexpectedly or beyond safe mechanical limits.

Mitigation: Confirm safe pulse-width ranges for the connected servo, avoid running the infinite loop as written, and keep hands and mechanisms clear during tests.

Risk: PWM chip, channel, and GPIO mappings vary across Raspberry Pi models.

Mitigation: Verify the target model, GPIO mode, pwmchip index, channel mapping, wiring, and power supply before applying commands.

## Reference(s):

- [Servo control troubleshooting guide](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hardware PWM setup steps, virtual environment installation guidance, servo control examples, and troubleshooting checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
