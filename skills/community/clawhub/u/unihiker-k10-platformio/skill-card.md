## Description:

Helps agents program UNIHIKER K10 boards with PlatformIO CLI, create or convert Arduino/C++ projects, build, upload, monitor serial output, diagnose setup or ASR issues, and prepare offline workshop installers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockets-cn](https://clawhub.ai/user/rockets-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workshop instructors use this skill to create, convert, build, upload, and troubleshoot PlatformIO-based Arduino/C++ projects for UNIHIKER K10 boards, including offline class setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workshop installers and build setup can install or execute unchecked mutable code across user machines.

Mitigation: Review the skill before workshop use, generate bundles from trusted sources, prefer pinned PlatformIO commits, and hash-verify Python wheels.

Risk: Removing macOS quarantine can bypass an operating-system safety control.

Mitigation: Remove quarantine only after verifying the installer source and distributing a freshly generated bundle.

Risk: Examples may activate camera, microphone, face recognition, or firmware flashing behavior.

Mitigation: Tell users before running those examples and confirm the selected workflow matches the board firmware and classroom policy.

Risk: K10 AI, voice, TTS, face recognition, or OTA projects can overwrite factory model-data regions if generic partitions are used.

Mitigation: Preserve the documented factory model, voice_data, and face-recognition flash offsets, and use separate USB initialization environments only when model recovery is needed.

## Reference(s):

- [PlatformIO Workshop Notes for UNIHIKER K10](references/platformio-workshop.md)
- [K10 AI Model Flashing and Recovery](references/k10-ai-model-flash.md)
- [K10 ASR Audio Troubleshooting](references/k10-asr-audio-troubleshooting.md)
- [K10 Arduino API](references/k10-arduino-api.md)
- [K10 Arduino Examples](references/k10-arduino-examples.md)
- [DFRobot PlatformIO Platform](https://github.com/DFRobot/platform-unihiker.git)
- [DFRobot Gravity ADS1115 Module](https://www.dfrobot.com.cn/goods-1734.html)
- [UNIHIKER K10 Arduino/PIO Example](https://www.unihiker.com.cn/wiki/k10/Arduino_PIO_Example)
- [UNIHIKER K10 Arduino/PIO API List](https://www.unihiker.com.cn/wiki/k10/Arduino_PIO_API_List)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash, PowerShell, INI, and C++ code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PlatformIO project files, command wrappers, and offline bundle or installer preparation steps when invoked.]

## Skill Version(s):

0.1.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
