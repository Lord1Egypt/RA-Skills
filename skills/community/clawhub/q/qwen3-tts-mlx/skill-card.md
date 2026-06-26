## Description: <br>
Local Qwen3-TTS speech synthesis on Apple Silicon via MLX for offline narration, audiobooks, video voiceovers, and multilingual TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h1bomb](https://clawhub.ai/user/h1bomb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and production teams use this skill to run local text-to-speech on Apple Silicon, including built-in voices, voice design, voice cloning, and batch dubbing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning can be used to imitate a person without consent. <br>
Mitigation: Use voice cloning only with voices you own or have explicit permission to use, and avoid impersonation or deceptive synthetic speech. <br>
Risk: Reference audio and transcripts may contain sensitive personal data. <br>
Mitigation: Treat reference audio and transcripts as sensitive data and limit storage, sharing, and reuse to approved workflows. <br>
Risk: The skill installs Python and Homebrew dependencies and downloads MLX models. <br>
Mitigation: Install only in environments where these dependencies and model downloads are approved. <br>


## Reference(s): <br>
- [Qwen3 Tts Mlx on ClawHub](https://clawhub.ai/h1bomb/qwen3-tts-mlx) <br>
- [Dubbing JSON Format](references/dubbing_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers local audio generation outputs such as WAV files, batch segment files, and merged dubbing audio.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
