## Description:

SenseAudio Floating Audio Assistant opens and manages an AudioClaw desktop assistant for macOS system-audio captions, ASR/translation, copied-text TTS, music generation, and transcript organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkzz1225](https://clawhub.ai/user/kkzz1225)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AudioClaw users use this skill to launch, stop, configure, and troubleshoot a macOS floating audio assistant that captures system audio for subtitles, ASR/translation, TTS, music generation, and transcript organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starting the assistant can capture system audio and send it to SenseAudio for processing.

Mitigation: Start it only when affected users have consented, and avoid sensitive meetings, private notifications, or protected media unless that data may be captured, stored in workspace state, and processed by SenseAudio.

Risk: The skill launches external workspace realtime interpreter scripts without integrity checks.

Mitigation: Install only in trusted AudioClaw workspaces, verify the external realtime interpreter toolchain before use, and protect those scripts from unauthorized modification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kkzz1225/skills/senseaudio-floating-audio-assistant)
- [README](README.md)
- [Quickstart](references/quickstart.md)
- [Operator Notes](references/operator_notes.md)
- [SenseAudio Integration](references/senseaudio_integration.md)
- [Troubleshooting](references/troubleshooting.md)
- [SenseAudio TTS endpoint](https://api.senseaudio.cn/v1/t2a_v2)
- [SenseAudio music generation endpoint](https://api.senseaudio.cn/v1/music/song/create)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and diagnostic JSON when running the smoke test]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS audio routing dependencies and SenseAudio credentials supplied by the host AudioClaw runtime.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
