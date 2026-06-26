## Description: <br>
Local text-to-speech using Piper voices via sherpa-onnx that runs offline without API keys and outputs Telegram-compatible voice notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stolot0mt0m](https://clawhub.ai/user/stolot0mt0m) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
OpenClaw users and agent builders use this skill to turn text replies into locally generated spoken audio for Telegram-style voice messages. It is useful when a response should be heard aloud without sending text to a cloud speech service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer is run with sudo and downloads third-party TTS binaries and voice models. <br>
Mitigation: Review the installer before execution and verify downloaded release artifacts where possible before using the skill. <br>
Risk: The security review notes that the expected bin/voice-reply command should be present and reviewable in the installed package. <br>
Mitigation: Confirm the command exists, inspect it, and test a local synthesis path before relying on the skill in an agent workflow. <br>


## Reference(s): <br>
- [Voice Reply on ClawHub](https://clawhub.ai/stolot0mt0m/voice-reply) <br>
- [Publisher profile](https://clawhub.ai/user/stolot0mt0m) <br>
- [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) <br>
- [Piper](https://github.com/rhasspy/piper) <br>
- [Piper voice samples](https://rhasspy.github.io/piper-samples/) <br>
- [Thorsten Voice](https://github.com/thorstenMueller/Thorsten-Voice) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [Text output containing an audio marker and MEDIA path for an OGG Opus voice file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emits [[audio_as_voice]] and MEDIA:/tmp/voice-reply-output.ogg for Telegram voice-note handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
