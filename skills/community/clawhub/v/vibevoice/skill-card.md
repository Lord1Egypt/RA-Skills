## Description:

Local Spanish TTS using Microsoft VibeVoice that generates natural voice audio from text, optimized for WhatsApp voice messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javier887](https://clawhub.ai/user/javier887)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to turn Spanish text into local voice-message audio for WhatsApp-style workflows, with voice, speed, and output-format options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags high-impact input-handling and dependency risks around the local script, dependency installation, model downloads, voice option, and environment variables.

Mitigation: Install only from trusted VibeVoice source checkouts, pin dependencies and upstream revisions before use, and avoid exposing voice names or environment variables to untrusted input.

Risk: The skill executes local shell, Python, PyTorch, and ffmpeg workflows that create media files on the host.

Mitigation: Review the script before installation, run it in a controlled local environment, and scan generated files and changed dependencies before deployment.

## Reference(s):

- [VibeVoice project homepage](https://github.com/microsoft/VibeVoice)
- [ClawHub skill page](https://clawhub.ai/javier887/skills/vibevoice)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local audio files in OGG, MP3, or WAV format; OGG is the default for WhatsApp voice-message use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
