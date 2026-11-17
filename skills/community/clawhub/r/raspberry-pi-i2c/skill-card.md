## Description:

Guides agents through Raspberry Pi I2C sensor development, including GPIO pin selection, hardware and software I2C tradeoffs, gpiod usage, BMI270 and MAX30205 driver notes, performance constraints, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntsmzt2009](https://clawhub.ai/user/ntsmzt2009)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and troubleshoot Raspberry Pi I2C sensor projects, especially systems using BMI270 IMUs, MAX30205 temperature sensors, standard /dev/i2c-1, or gpiod-based software I2C.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An overbroad privileged process command may stop unrelated Python services on the device.

Mitigation: Review commands before execution; replace `sudo killall python3` with targeted process identification and stop only the process holding the GPIO or I2C resource.

Risk: Unpinned Python package installation can produce unreproducible behavior across devices.

Mitigation: Use a virtual environment and pin dependency versions before installing GPIO or SMBus libraries.

Risk: Incorrect voltage wiring can damage Raspberry Pi GPIO pins.

Mitigation: Verify sensor logic levels before connecting hardware; use 3.3V-compatible devices or level shifting for 5V signals.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ntsmzt2009/skills/raspberry-pi-i2c)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [pinout.xyz Interactive Pinout](https://pinout.xyz/)
- [BMI270 Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi270-ds000.pdf)
- [BMI270 Sensor API](https://github.com/boschsensortec/BMI270-Sensor-API)
- [MAX30205 Product Page](https://www.analog.com/en/products/max30205.html)
- [libgpiod Documentation](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with tables, checklists, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hardware wiring notes, command examples, Python and C snippets, performance notes, and troubleshooting checklists.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
