## Description:

Helps agents build, upload, and debug PlatformIO Arduino/C++ projects for the UNIHIKER K10 experiment box, including LVGL dashboards, QMI8658 motion controls, audio FFT visualizers, actuators, and K10-versus-box hardware boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockets-cn](https://clawhub.ai/user/rockets-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and hardware engineers use this skill to create or troubleshoot K10 Box PlatformIO projects that combine Arduino/C++ firmware, LVGL displays, K10-native sensors, experiment-box sensors, audio processing, and actuator behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote PlatformIO and driver inputs may change or be downloaded without independent integrity checks.

Mitigation: Review or pin the PlatformIO platform and verify downloaded driver file hashes before building or uploading firmware.

Risk: Firmware built with this guidance can operate motors, LEDs, and a buzzer on connected K10 Box hardware.

Mitigation: Run actuator tests only after explicit user action, confirm the box IO controller is present, keep the device in a safe physical setup, and stop all outputs after tests.

## Reference(s):

- [K10 Box Hardware Map](references/hardware-map.md)
- [LVGL Dashboard and Actuator Patterns](references/lvgl-dashboard.md)
- [K10 Box Audio FFT and Reactive Lights](references/audio-fft.md)
- [QMI8658 Six-Axis LVGL Games](references/six-axis-games.md)
- [K10 Box Troubleshooting](references/troubleshooting.md)
- [DFRobot UNIHIKER PlatformIO Platform](https://github.com/DFRobot/platform-unihiker.git)
- [DFRobot K10 Box Extension Repository](https://gitee.com/zhaoruiz/ext-unihiker-k10-box)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Arduino/C++ code, shell commands, configuration snippets, and diagnostic checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PlatformIO setup steps, firmware snippets, hardware safety checks, and runtime verification guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
