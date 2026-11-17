## Description:

A local text-to-speech and voice-cloning skill that guides agents through installing dependencies, using Qwen3-TTS with MLX Audio, and generating speech or cloned-voice audio on Apple Silicon macOS systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsalfkjaklsdfjqw](https://clawhub.ai/user/dsalfkjaklsdfjqw)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creators use this skill to set up local TTS and voice-cloning workflows for audiobooks, character voices, voice assistants, accessibility applications, video narration, and multilingual dubbing. The skill is intended for users who can review and run macOS shell commands and Python examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run remote installer code and fetch unpinned packages or models.

Mitigation: Prefer manual, reviewed installation steps; pin dependency and model versions where possible before deployment.

Risk: The skill presents itself as local and offline, but initial installation and model acquisition may require network access.

Mitigation: Plan for a reviewed online setup phase, then verify local operation before using sensitive audio or text.

Risk: Voice cloning can be misused to impersonate people or process voice data without consent.

Mitigation: Clone only voices the user owns or has explicit permission to use, and review generated audio for lawful and non-deceptive use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dsalfkjaklsdfjqw/skills/qwen3-free-tts)
- [OpenClaw voice cloning documentation](https://docs.openclaw.ai/skills/voice-cloning)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included demo script can produce WAV audio files when run in a prepared local environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
