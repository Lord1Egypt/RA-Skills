## Description:

基于双引擎策略的智能语音系统，支持中文本地 Tingting 语音和多语言 Edge-TTS 云端语音，输出高质量 OGG 音频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackytianjp](https://clawhub.ai/user/jackytianjp)

### License/Terms of Use:

MIT License

## Use Case:

Developers and agent builders use this skill to generate spoken audio for a Xiaoye AI companion workflow, using local macOS Chinese speech when available and Edge-TTS for other supported languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Non-Chinese input may be processed by Microsoft Edge-TTS cloud services.

Mitigation: Avoid confidential text unless use is restricted to the local Chinese macOS path or a local-only control is added.

Risk: Telegram integration can upload generated audio to Telegram.

Mitigation: Review generated audio and destination chat handling before using Telegram delivery with sensitive content.

Risk: The optional edge-tts dependency is declared with a minimum version only.

Mitigation: Pin edge-tts to a reviewed version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackytianjp/skills/xiaoye-voice)
- [Publisher profile](https://clawhub.ai/user/jackytianjp)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces local audio files, usually OGG, under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
