## Description: <br>
Use when programming Unihiker K10 board with Arduino/C++, uploading code, flashing firmware, or accessing K10 Arduino APIs for screen, sensors, RGB, audio, AI, TTS, and ASR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockets-cn](https://clawhub.ai/user/rockets-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and educators use this skill to set up an Arduino CLI workflow for Unihiker K10 boards, compile and upload Arduino/C++ sketches, troubleshoot ports, and reference K10 screen, sensor, audio, AI, TTS, and ASR APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup workflow can modify the local Arduino environment and may run an upstream Arduino CLI installer without pinning or verification. <br>
Mitigation: Review setup.sh before use, install Arduino CLI from a pinned release or package manager when possible, and run setup steps only in an environment where Arduino configuration changes are acceptable. <br>
Risk: Camera, speech, and face-recognition examples may process sensitive image, biometric, or audio data when adapted for real projects. <br>
Mitigation: Add explicit consent, privacy notices, retention limits, and local data-handling safeguards before reusing those examples beyond local experimentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rockets-cn/unihiker-k10-arduino) <br>
- [Arduino API reference](references/arduino-api.md) <br>
- [Arduino examples](references/arduino-examples.md) <br>
- [Arduino CLI releases](https://github.com/arduino/arduino-cli/releases) <br>
- [DFRobot Unihiker board package index](https://downloadcd.dfrobot.com.cn/UNIHIKER/package_unihiker_index.json) <br>
- [Espressif ESP32 Arduino package index](https://dl.espressif.com/dl/package_esp32_index.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Arduino/C++ code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, upload, troubleshooting, offline bundle, and API reference guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
