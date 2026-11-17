## Description:

把文字转成语音。可以发语音、念给我听、唱歌、用方言或夹子音说话，支持各种情绪和风格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangalexhy](https://clawhub.ai/user/zhangalexhy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to synthesize Chinese or English speech from text through the MiMo/Xiaomi TTS service, with options for voice, style, emotion, character, dialect, and output WAV handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis and the MiMo API credential are sent to an external MiMo/Xiaomi TTS service.

Mitigation: Avoid using secrets, private personal data, regulated data, or text that should not be processed by that provider.

Risk: The skill may read a MiMo API key from ~/.openclaw/config.json when no key is passed explicitly.

Mitigation: Prefer passing credentials explicitly for controlled runs and review local OpenClaw configuration before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangalexhy/skills/xiaomi-tts)
- [MiMo TTS API endpoint](https://api.xiaomimimo.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Command-line usage guidance and WAV audio output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write WAV audio to a file or stream audio bytes to stdout; requires a MiMo API key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
