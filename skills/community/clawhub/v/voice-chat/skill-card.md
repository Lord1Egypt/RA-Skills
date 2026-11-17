## Description:

Voice Chat Bridge automatically handles voice or audio messages by transcribing speech, using conversation context to draft a reply, and generating a spoken response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangqinghua2015](https://clawhub.ai/user/zhangqinghua2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add voice-message workflows that convert incoming audio to text, generate a context-aware reply, and return an OGG/Opus voice response for channels such as Feishu or Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic voice handling can process private chat audio and current conversation context without clear user consent or channel boundaries.

Mitigation: Use the skill only with explicit user consent and scope automation to trusted channels and users.

Risk: Transcripts, generated replies, or logs may expose sensitive chat content.

Mitigation: Disable or restrict content logging and avoid reusing privileged sessions for transcript replies.

Risk: Downloaded speech-recognition models and runtime dependencies may be unverified.

Mitigation: Verify downloaded models and dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangqinghua2015/skills/voice-chat)
- [README](artifact/README.md)
- [Design Document](artifact/DESIGN.md)
- [Changelog](artifact/CHANGELOG.md)
- [Sherpa-ONNX SenseVoice Model Download](https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2)
- [Vosk Chinese Small Model Download](https://github.com/alphacep/vosk-api/releases/download/v0.3.45/vosk-model-small-cn-0.22.zip)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime scripts emit text, JSON status, and generated OGG/Opus voice-file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local temporary files under /tmp/voice-chat and depends on configured STT/TTS engines.]

## Skill Version(s):

2.3.5 (source: server release metadata and changelog, released 2026-04-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
