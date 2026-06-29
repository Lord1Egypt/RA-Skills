## Description: <br>
Use when programming a UNIHIKER K10 board with PlatformIO CLI, creating or converting Arduino/C++ K10 projects to PlatformIO, building, uploading, monitoring serial output, diagnosing K10 PlatformIO setup, or preparing/installing offline PlatformIO support bundles for workshops where many students should not download toolchains at the same time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockets-cn](https://clawhub.ai/user/rockets-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and workshop facilitators use this skill to create, convert, build, upload, and troubleshoot UNIHIKER K10 PlatformIO Arduino/C++ projects. It also helps prepare offline PlatformIO support bundles for classroom or workshop environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera, microphone, face recognition, speech recognition, or TTS examples may create privacy concerns in classrooms or shared spaces. <br>
Mitigation: Get consent before using those examples, make camera and microphone activity obvious, and use the examples only in settings appropriate for participants. <br>
Risk: Offline bundles are extracted into the PlatformIO tool directory and could overwrite or introduce local toolchain files if the bundle is untrusted. <br>
Mitigation: Use only trusted offline bundles, prepare one bundle per OS and CPU architecture, and verify the installed PlatformIO packages before workshop use. <br>
Risk: Incorrect OTA partition choices for AI projects can overwrite K10 model, voice data, or face-recognition regions. <br>
Mitigation: Use the model-preserving partition guidance from the bundled K10 AI model flashing reference when a project uses built-in AI features. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rockets-cn/unihiker-k10-platformio) <br>
- [PlatformIO Workshop Notes for UNIHIKER K10](references/platformio-workshop.md) <br>
- [K10 AI Model Flashing and Recovery](references/k10-ai-model-flash.md) <br>
- [UNIHIKER K10 Arduino API](references/k10-arduino-api.md) <br>
- [UNIHIKER K10 Arduino Examples](references/k10-arduino-examples.md) <br>
- [DFRobot PlatformIO Platform for UNIHIKER](https://github.com/DFRobot/platform-unihiker.git) <br>
- [PlatformIO Core Installer Script Documentation](https://docs.platformio.org/en/latest/core/installation/methods/installer-script.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, PlatformIO configuration, and C++ code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose project files, PlatformIO commands, offline bundle steps, and K10-specific implementation guidance.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
