## Description:

豆包语音合成 2.0，支持情绪控制、多音色、语音指令。34 种音色可选，含 JARVIS 同款男声。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanmomuyu-sys](https://clawhub.ai/user/yanmomuyu-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users use this skill to generate Chinese and English speech audio from text through Volcengine/ByteDance SeedTTS 2.0. It supports voice selection, emotional speech tags, command-line use, Python SDK calls, and batch audio generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synthesis text and Volcengine credentials can be sent to Volcengine/ByteDance or to a configured endpoint.

Mitigation: Use the skill only with text appropriate for external cloud processing, avoid regulated or secret content in requests, and store the Volcengine token using the intended environment or OpenClaw configuration mechanism.

Risk: A custom VOLCANO_API_URL can redirect requests to an untrusted destination.

Mitigation: Leave VOLCANO_API_URL unset unless the destination is fully trusted and reviewed.

Risk: Windows playback uses a shell-based playback path identified by the security evidence.

Mitigation: Avoid the playback option on Windows until that path is fixed; generate audio files and play them manually with a trusted player instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanmomuyu-sys/skills/seedtts2)
- [Volcengine speech console](https://console.volcengine.com/speech)
- [Volcengine TTS API endpoint](https://openspeech.bytedance.com/api/v3/tts/unidirectional)
- [Voice library](docs/voice-library.md)
- [Troubleshooting guide](docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Files, API Calls, Shell commands, Code, Configuration instructions]

**Output Format:** [Audio files with command-line or Python SDK status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MP3 or WAV audio, supports batch output, and requires Volcengine APP ID and Access Token configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
