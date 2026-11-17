## Description:

Use when programming Unihiker K10 board with Arduino/C++, uploading code, flashing firmware, or accessing K10 Arduino APIs for screen, sensors, RGB, audio, AI, TTS, and ASR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockets-cn](https://clawhub.ai/user/rockets-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hardware engineers use this skill to configure Arduino tooling, compile and upload sketches, troubleshoot board connectivity, and look up Unihiker K10 Arduino APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and flashing scripts may use unsafe installation or device-targeting shortcuts.

Mitigation: Review scripts before execution, avoid elevated privileges, install arduino-cli from a pinned release or trusted package manager, and explicitly specify serial ports and OTA IP addresses.

Risk: Offline bundles can introduce untrusted board packages or tooling.

Mitigation: Use only offline bundles from a trusted source and verify their contents before installing them.

Risk: Audio, camera, and face-recognition examples can process privacy-sensitive data.

Mitigation: Confirm user consent and local privacy requirements before running examples that capture audio, images, or face data.

## Reference(s):

- [Arduino API Reference](references/arduino-api.md)
- [Arduino Examples](references/arduino-examples.md)
- [Arduino CLI Releases](https://github.com/arduino/arduino-cli/releases)
- [UNIHIKER K10 Arduino PIO Example](https://www.unihiker.com.cn/wiki/k10/Arduino_PIO_Example)
- [UNIHIKER K10 Arduino PIO API List](https://www.unihiker.com.cn/wiki/k10/Arduino_PIO_API_List)
- [DFRobot Gravity I2C ADS1115 ADC Module](https://www.dfrobot.com.cn/goods-1734.html)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Arduino/C++ code blocks, shell commands, PowerShell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device-specific serial port, OTA IP address, firmware, and board package guidance.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
