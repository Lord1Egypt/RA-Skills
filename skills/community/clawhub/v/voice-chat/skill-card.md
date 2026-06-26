## Description: <br>
Automatically processes voice messages by transcribing audio, generating a context-aware reply, and synthesizing a voice response when voice or audio messages are received. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangqinghua2015](https://clawhub.ai/user/zhangqinghua2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to bridge chat voice messages into text, generate a concise agent reply using the current conversation context, and return a synthesized voice response for Feishu or Telegram workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on voice processing and automatic replies can respond in chats where the user did not intend to enable automation. <br>
Mitigation: Enable the trigger only for trusted chats or users and require clear channel and sender scoping before automatic replies are sent. <br>
Risk: Voice transcripts and generated replies may contain sensitive content that can be sent to the active LLM provider or Edge TTS. <br>
Mitigation: Decide which providers may receive sensitive text, prefer local fallbacks where appropriate, and suppress transcript and reply logging where possible. <br>
Risk: Speech models and Python dependencies are downloaded separately and can affect integrity and runtime behavior. <br>
Mitigation: Use pinned dependencies, verified model downloads, and local review before deployment. <br>


## Reference(s): <br>
- [ClawHub Voice Chat Bridge release page](https://clawhub.ai/zhangqinghua2015/voice-chat) <br>
- [Sherpa-ONNX SenseVoice model release](https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2) <br>
- [Vosk Chinese small model release](https://github.com/alphacep/vosk-api/releases/download/v0.3.45/vosk-model-small-cn-0.22.zip) <br>
- [Telegram Bot API](https://api.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text transcripts and replies, JSON status objects, and OGG/Opus audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Temporary audio outputs are written under /tmp/voice-chat; operation depends on ffmpeg, downloaded STT models, a TTS engine, and OpenClaw session context.] <br>

## Skill Version(s): <br>
2.3.5 (source: server evidence and changelog, released 2026-04-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
