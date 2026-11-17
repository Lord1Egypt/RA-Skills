## Description:

Smart Telegram reply workflow for OpenClaw: if the user sends text, reply with text; if the user sends a voice note/audio, transcribe locally using the installed mlx_audio, then generate a meaningful reply in the same language and return a single Telegram voice note with matching caption when voice output is requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengling9405](https://clawhub.ai/user/pengling9405)

### License/Terms of Use:


## Use Case:

Developers and Telegram automation users use this skill to handle multilingual OpenClaw replies where text inputs stay text-only and voice inputs are transcribed locally before producing either text or a single voice message with an identical caption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Telegram audio, generated speech, and transcript data can remain on disk after local ASR or TTS processing.

Mitigation: Run the skill only on a trusted machine and account, review temporary-file retention before deployment, and patch cleanup or manually clear the temporary directories after use.

Risk: Voice replies can mislead users if the spoken audio and visible caption diverge.

Mitigation: Keep the caption identical to the generated reply text used for TTS and review voice outputs before automated use in sensitive conversations.

## Reference(s):

- [Qwen3-ASR mlx_audio quick notes](references/qwen3-asr-notes.md)
- [mlx_audio Qwen3-ASR upstream README](https://github.com/Blaizzy/mlx-audio/blob/main/mlx_audio/stt/models/qwen3_asr/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; runtime helpers can emit plain text, JSON, SRT, VTT, and OGG/Opus audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice replies require the caption text to match the synthesized voice content exactly.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
