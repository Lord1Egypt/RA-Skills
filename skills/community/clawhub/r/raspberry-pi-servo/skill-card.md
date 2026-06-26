## Description: <br>
Guides an agent through enabling Raspberry Pi hardware PWM and controlling servos with the rpi-hardware-pwm Python library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CLD1994](https://clawhub.ai/user/CLD1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hardware engineers use this skill when configuring Raspberry Pi hardware PWM for precise servo control. It helps agents propose setup checks, boot configuration changes, Python environment setup, example PWM code, and troubleshooting steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Boot configuration edits and reboot steps can disrupt a Raspberry Pi if applied incorrectly. <br>
Mitigation: Back up the boot configuration, review exact file paths for the installed Raspberry Pi OS version, and require explicit user approval before sudo commands or reboot. <br>
Risk: Servo tests can move hardware unexpectedly or draw insufficient power. <br>
Mitigation: Secure the servo before testing, verify wiring and external 5V power, and stop or disable PWM when finished. <br>
Risk: Installing or using the Python PWM package from an unverified source can introduce dependency risk. <br>
Mitigation: Verify the rpi-hardware-pwm package source and version before installation, preferably inside a Python virtual environment. <br>


## Reference(s): <br>
- [Servo Control Troubleshooting Guide](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/CLD1994/raspberry-pi-servo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent guidance may include sudo commands, boot configuration edits, and servo troubleshooting steps that require user approval and hardware verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
