## Description: <br>
豆包语音合成 2.0，支持情绪控制、多音色、语音指令。34 种音色可选，含 JARVIS 同款男声。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanmomuyu-sys](https://clawhub.ai/user/yanmomuyu-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to configure Volcengine/Bytedance Doubao SeedTTS 2.0 credentials, select voices, synthesize Chinese or English speech, and generate MP3/WAV output from command-line or Python workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends synthesis text and TTS credentials to a disclosed remote provider. <br>
Mitigation: Install and use it only when Volcengine/Bytedance is an acceptable processor for the text being synthesized and the associated access token. <br>
Risk: TTS access tokens can be exposed through plaintext configuration or shared debug output. <br>
Mitigation: Prefer environment variables or a secret manager, avoid committing OpenClaw configuration files with secrets, and redact VOLCANO_ACCESS_TOKEN from logs and support messages. <br>
Risk: Local playback behavior can be sensitive when output filenames or speaker IDs are influenced by untrusted input, especially on Windows. <br>
Mitigation: Use trusted speaker IDs and output paths, review generated filenames before playback, and avoid passing untrusted values into playback workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yanmomuyu-sys/seedtts2) <br>
- [Volcengine speech console](https://console.volcengine.com/speech) <br>
- [Bytedance OpenSpeech TTS endpoint](https://openspeech.bytedance.com/api/v3/tts/unidirectional) <br>
- [Voice library](docs/voice-library.md) <br>
- [Troubleshooting guide](docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, audio files] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, configuration snippets, and generated MP3/WAV file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is saved locally; the skill sends synthesis text and credentials to the configured Volcengine/Bytedance TTS endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
