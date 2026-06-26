## Description: <br>
Provides debugging support for Zhengzhou Keweilai stepper motor controllers, including technical documentation plus MicroPython and Python code for Modbus RTU register reads, writes, homing, and movement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbs2016](https://clawhub.ai/user/lbs2016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to generate operating guidance and example code for configuring, testing, and controlling a Zhengzhou Keweilai stepper motor controller over Modbus RTU. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated code can move connected hardware and change controller settings. <br>
Mitigation: Verify wiring, serial port, device address, limits, travel bounds, and emergency-stop access before running movement or write operations. <br>
Risk: Arbitrary register writes can alter operating parameters such as speed, address, limits, and homing behavior. <br>
Mitigation: Review register addresses and values with an operator before applying writes, especially on production equipment. <br>
Risk: Movement helpers can exceed safe travel if the controller is not homed or limit switches are not functioning. <br>
Mitigation: Confirm mechanical homing, limit-switch status, and maximum travel constraints before executing automated movement sequences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lbs2016/zhengzhou-keweilai-stepping-moto-controller-help) <br>
- [Skill source instructions](artifact/SKILL.md) <br>
- [Technical documentation](artifact/documentation.md) <br>
- [Configuration metadata](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown documentation plus Python and MicroPython code for Modbus RTU register operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hardware register writes and movement helper code for a connected stepper motor controller.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
