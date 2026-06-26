## Description: <br>
XiaoZhi AI Device (ESP32) integration for OpenClaw that enables real-time voice interaction with an AI assistant through XiaoZhi hardware using a WebSocket bridge, Volcengine Doubao STT/TTS, and Opus audio streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect XiaoZhi ESP32 hardware as a voice channel for hands-free conversations, voice commands, and basic device interaction with OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live microphone audio, transcripts, and generated speech may be processed by Volcengine Doubao or the configured provider without a clear privacy or consent notice. <br>
Mitigation: Require a clear privacy notice, explicit user or administrator opt-in, documented data flow, and an option to disable or replace remote STT/TTS processing for sensitive conversations. <br>
Risk: The skill requires STT/TTS provider credentials for operation. <br>
Mitigation: Store credentials in environment variables, avoid committing environment files, restrict credential access, and rotate credentials according to the provider's operational policy. <br>


## Reference(s): <br>
- [Xiaozhi Claw on ClawHub](https://clawhub.ai/leohuang8688/xiaozhiclaw) <br>
- [XiaoZhi AI ESP32 Project](https://github.com/xiaozhi-ai) <br>
- [Volcengine Doubao API](https://www.volcengine.com/) <br>
- [Volcengine Speech Recognition API](https://www.volcengine.com/docs/6561/142162) <br>
- [Volcengine Text-to-Speech API](https://www.volcengine.com/docs/6561/142164) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [Opus Audio Codec](https://opus-codec.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Audio, Configuration, Guidance] <br>
**Output Format:** [WebSocket messages, transcribed text, synthesized speech audio, and Markdown configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XiaoZhi ESP32 hardware, WebSocket network access, Opus audio handling, and configured STT/TTS provider credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
