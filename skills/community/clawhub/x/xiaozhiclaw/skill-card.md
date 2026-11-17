## Description:

XiaoZhi AI Device (ESP32) integration for OpenClaw, enabling real-time voice interaction with an AI assistant through XiaoZhi hardware using a WebSocket bridge, Volcengine Doubao STT/TTS, and Opus audio streaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect XiaoZhi ESP32 hardware as a voice channel for hands-free conversations with an OpenClaw agent. It supports device audio streaming, speech-to-text, text-to-speech, and basic voice interaction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an unauthenticated WebSocket path into the agent.

Mitigation: Use only on a trusted, isolated network unless device authentication, pairing enforcement, WSS/TLS, and payload limits are added.

Risk: The skill handles microphone audio, transcripts, generated responses, and Doubao credentials.

Mitigation: Review data handling before installation, set credentials only through environment variables, redact logs, and assume voice/text data may be sent to Volcengine Doubao.

Risk: The scanner verdict is suspicious because sensitive voice and text data are handled with weak controls.

Mitigation: Review and test the skill before deployment, especially recording limits, logging behavior, network exposure, and device pairing behavior.

## Reference(s):

- [Xiaozhi Claw ClawHub Release](https://clawhub.ai/leohuang8688/skills/xiaozhiclaw)
- [XiaoZhi AI ESP32 Project](https://github.com/xiaozhi-ai)
- [Volcengine Doubao API](https://www.volcengine.com/)
- [Volcengine Speech-to-Text API](https://www.volcengine.com/docs/6561/142162)
- [Volcengine Text-to-Speech API](https://www.volcengine.com/docs/6561/142164)
- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [Opus Audio Codec](https://opus-codec.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include WebSocket configuration, environment variable setup, device connection steps, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
