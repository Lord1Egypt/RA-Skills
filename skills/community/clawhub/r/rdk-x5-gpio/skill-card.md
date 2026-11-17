## Description:

Guides agents in controlling RDK X5 40-pin interfaces for GPIO digital I/O, PWM devices, I2C and SPI sensors, UART serial communication, CAN bus setup, and pinout checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hardware engineers use this skill to ask an agent for RDK X5 40-pin peripheral commands, wiring guidance, setup checks, and troubleshooting for GPIO, PWM, I2C, SPI, UART, and CAN workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root-level hardware commands and bus writes can affect connected RDK X5 peripherals or live equipment.

Mitigation: Verify the board model, pin mapping, voltage levels, attached devices, bus addresses, CAN bitrate, and test-state readiness before executing commands.

Risk: Sample I2C, CAN, and sudo commands may be unsafe when copied directly onto production or shared hardware.

Mitigation: Review sample scripts and commands before use, avoid arbitrary I2C writes or CAN sends on live systems, and prefer pinned or OS-vendor packages for spidev.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/skills/rdk-x5-gpio)
- [Publisher profile](https://clawhub.ai/user/katherineedwards2475)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command and wiring guidance; it does not author full application scripts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
