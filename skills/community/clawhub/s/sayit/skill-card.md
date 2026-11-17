## Description:

Text-to-speech using Kokoro local TTS. Use when the user wants to convert text to audio, read aloud, or generate speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[babysor](https://clawhub.ai/user/babysor)

### License/Terms of Use:


## Use Case:

Developers, creators, and other external users use this skill to generate local speech audio from text, documents, EPUB/PDF inputs, or streams with selectable Kokoro voices and output formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on an external kokoro-tts package and GitHub-hosted model assets.

Mitigation: Install only from trusted sources, pin the package version where practical, and verify model-file checksums before use.

Risk: The skill can process local text, EPUB, and PDF files supplied by the user.

Mitigation: Run with normal user permissions and convert only files the user intends to process.

## Reference(s):

- [Kokoro TTS Reference](artifact/reference.txt)
- [Kokoro TTS project](https://github.com/nazdridoy/kokoro-tts)
- [Kokoro ONNX model release asset](https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/kokoro-v1.0.onnx)
- [Kokoro voices release asset](https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/voices-v1.0.bin)
- [ClawHub skill page](https://clawhub.ai/babysor/skills/sayit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of audio files or streamed playback through local Kokoro TTS commands.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
