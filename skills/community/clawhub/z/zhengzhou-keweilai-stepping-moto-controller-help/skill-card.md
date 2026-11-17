## Description:

Provides debugging support for a Zhengzhou Keweilai stepper motor controller, including register guidance, Markdown technical documentation, and Python/MicroPython demo code for Modbus RTU control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs2016](https://clawhub.ai/user/lbs2016)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and automation operators use this skill to generate controller documentation and example code, read and write Modbus RTU registers, and debug stepper motor movement, homing, limit status, and emergency-stop workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly move physical hardware and change controller settings.

Mitigation: Use it only with supervised hardware, tested limit switches, an independent emergency stop, and explicit confirmation before movement or controller-setting writes.

Risk: Unsafe travel limits, speed values, communication failures, or unverified controller state can cause unintended motion.

Mitigation: Validate travel limits, speed ranges, communication errors, and controller state before each movement, and stop operation if checks fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lbs2016/skills/zhengzhou-keweilai-stepping-moto-controller-help)
- [Artifact documentation](artifact/documentation.md)
- [Artifact configuration](artifact/config.json)
- [PC Python driver](artifact/python_driver.py)
- [MicroPython driver](artifact/micropython_driver.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and code snippets for Python, MicroPython, and Modbus RTU configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hardware-control steps that read or write controller registers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
