## Description: <br>
Guides agents through RDK X5 40-pin GPIO, PWM, I2C, SPI, UART, and CAN control with wiring guidance, Python snippets, and shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to control RDK X5 40-pin peripherals, configure hardware interfaces, and troubleshoot GPIO, PWM, I2C, SPI, UART, and CAN workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can change physical device state through sudo, PWM output, I2C writes, serial writes, CAN sends, and sample scripts. <br>
Mitigation: Run examples only when you intend to control RDK X5 hardware and have verified the connected devices and expected behavior. <br>
Risk: Incorrect pinout, voltage level, current limit, pull-up, bus number, device address, or connected load assumptions can damage hardware or produce unsafe motion. <br>
Mitigation: Verify the board pinout, voltage levels, current limits, pull-ups, bus numbers, device addresses, drivers, and connected loads before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/rdk-x5-gpio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides commands and wiring guidance; does not produce full scripts by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
