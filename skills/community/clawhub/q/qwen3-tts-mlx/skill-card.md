## Description:

Local Qwen3-TTS speech synthesis on Apple Silicon via MLX. Use for offline narration, audiobooks, video voiceovers, and multilingual TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h1bomb](https://clawhub.ai/user/h1bomb)

### License/Terms of Use:


## Use Case:

Developers, creators, and media teams use this skill to run local text-to-speech on Apple Silicon for narration, audiobooks, podcasts, video voiceovers, multilingual speech, voice design, and voice cloning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning can be used without consent and may enable impersonation.

Mitigation: Use voice cloning only with the speaker's informed permission and review generated speech before publication or distribution.

Risk: Reference audio, transcripts, and batch input JSON can contain sensitive personal or production content.

Mitigation: Avoid sensitive reference material, keep inputs local, and review output directories because batch processing copies the input JSON into the output folder.

Risk: The skill depends on a local ML audio stack and model downloads.

Mitigation: Install only in environments where dependency and model download risks are acceptable, and review the local runtime before deployment.

## Reference(s):

- [Qwen3 Tts Mlx on ClawHub](https://clawhub.ai/h1bomb/skills/qwen3-tts-mlx)
- [Dubbing JSON Format](references/dubbing_format.md)
- [Qwen3-TTS CustomVoice MLX model](https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-4bit)
- [Qwen3-TTS VoiceDesign MLX model](https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-5bit)
- [Qwen3-TTS Base MLX model](https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-0.6B-Base-4bit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python examples, JSON examples, and generated audio file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to generate local WAV audio through CLI or Python workflows and can produce batch dubbing outputs.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact frontmatter version is 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
