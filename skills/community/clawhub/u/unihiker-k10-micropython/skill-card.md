## Description:

Use when programming Unihiker K10 board with MicroPython, uploading code, flashing firmware, or accessing K10 MicroPython APIs (screen, sensors, RGB, audio, AI).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockets-cn](https://clawhub.ai/user/rockets-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to work with Unihiker K10 boards: uploading MicroPython code, flashing MicroPython firmware, detecting serial ports, troubleshooting connectivity, and looking up K10 APIs for screen, sensor, RGB, audio, and AI features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script can run live downloaded installer code, install unpinned packages, alter Arduino configuration, and possibly request system-wide installation privileges.

Mitigation: Review scripts/setup.sh before running it, use a sandbox where practical, pin and verify dependencies, and prefer user-local installation.

Risk: Example workflows can involve audio recording, face recognition, HID keystrokes, or sample WiFi/MQTT credentials.

Mitigation: Review examples before deployment, remove or replace sample credentials, and confirm privacy and device-control behavior for the intended environment.

## Reference(s):

- [MicroPython API reference](references/micropython-api.md)
- [DFRobot Gravity I2C ADS1115 16-bit ADC module](https://www.dfrobot.com.cn/goods-1734.html)
- [Arduino CLI installation documentation](https://arduino.github.io/arduino-cli/latest/installation/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide host setup, firmware flashing, MicroPython upload, device port detection, and K10 API usage.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
