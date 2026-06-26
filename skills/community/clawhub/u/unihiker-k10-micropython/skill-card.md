## Description: <br>
Use when programming Unihiker K10 board with MicroPython, uploading code, flashing firmware, or accessing K10 MicroPython APIs for screen, sensors, RGB, audio, and AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockets-cn](https://clawhub.ai/user/rockets-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hardware engineers use this skill to prepare a K10 development environment, detect serial ports, flash MicroPython firmware, upload Python files, and consult K10 MicroPython API guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script may install developer tools from network sources and change local Arduino and Python tooling. <br>
Mitigation: Review setup.sh before execution, run it in a controlled development environment, and approve network installers, sudo fallback, Python package changes, and Arduino CLI configuration changes. <br>
Risk: Tool installation and Arduino CLI configuration can leave persistent files and caches on the developer machine. <br>
Mitigation: Use a disposable or dedicated environment when possible, and inspect the configured K10 and Arduino paths before reusing the environment. <br>
Risk: Firmware flashing changes the attached K10 board state. <br>
Mitigation: Confirm the target serial port, board mode, and intended MicroPython firmware before flashing. <br>


## Reference(s): <br>
- [K10 MicroPython API Reference](references/micropython-api.md) <br>
- [DFRobot UNIHIKER Board Manager Package Index](https://downloadcd.dfrobot.com.cn/UNIHIKER/package_unihiker_index.json) <br>
- [Arduino CLI Installation](https://arduino.github.io/arduino-cli/latest/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and MicroPython code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local scripts and device-specific serial ports.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
