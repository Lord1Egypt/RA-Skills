## Description: <br>
Configures and uses Raspberry Pi GPIO for simple peripherals such as LEDs, buttons, servos, motors, and direct GPIO control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CLD1994](https://clawhub.ai/user/CLD1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hardware engineers use this skill to set up Raspberry Pi GPIO libraries and produce practical Python examples for buttons, LEDs, PWM, servos, interrupts, and basic GPIO troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GPIO wiring mistakes or incorrect voltage can damage Raspberry Pi hardware or connected components. <br>
Mitigation: Follow the wiring and voltage warnings in the artifact, use resistors for LEDs, avoid 5V on 3.3V components, and use a motor driver or H-bridge instead of connecting motors directly to GPIO pins. <br>
Risk: Package installation, removal, or user-group commands can change the host Raspberry Pi environment. <br>
Mitigation: Review sudo apt and usermod commands before execution, confirm the board model and existing package state, and choose rpi-lgpio or RPi.GPIO according to Raspberry Pi hardware compatibility. <br>
Risk: Software-timed servo control can jitter and may be unsuitable for long-running or precise motion control. <br>
Mitigation: Use the lgpio servo examples only for testing and prefer hardware PWM for sustained or precise servo operation. <br>


## Reference(s): <br>
- [Raspberry Pi GPIO and the 40-pin Header](references/raspberry-pi-gpio.md) <br>
- [GPIO Zero documentation](https://gpiozero.readthedocs.io) <br>
- [rpi-lgpio documentation](https://rpi-lgpio.readthedocs.io) <br>
- [Raspberry Pi physical computing motor control guidance](https://projects.raspberrypi.org/en/projects/physical-computing/14) <br>
- [ClawHub skill page](https://clawhub.ai/CLD1994/raspberry-pi-gpio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes hardware setup guidance, package installation commands, GPIO pin reference material, and safety notes for wiring and voltage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
