## Description:

Offline speech-to-text (ASR) using whisper.cpp (whisper-cli) + ffmpeg. Supports batch transcription, timestamps, SRT/TXT/JSON outputs, and model download. Cross-platform: macOS/Linux; Windows via WSL2 (recommended).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vvusu](https://clawhub.ai/user/vvusu)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and operators use this skill to transcribe local audio files or directories with whisper.cpp and ffmpeg, producing transcripts, subtitles, or structured text for review and downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer scripts can change system packages using sudo or package-manager commands.

Mitigation: Review install.sh before running it, or install ffmpeg and whisper-cli manually from trusted package sources.

Risk: Whisper model files may be downloaded without effective integrity checks when configured hashes are empty.

Mitigation: Pin model filenames and verify model checksums before using downloaded binaries.

Risk: Transcript outputs can contain sensitive speech content.

Mitigation: Store transcript files in access-controlled locations and delete local outputs when they are no longer needed.

## Reference(s):

- [Whisper.cpp GitHub](https://github.com/ggml-org/whisper.cpp)
- [Whisper.cpp Model Repository](https://huggingface.co/ggerganov/whisper.cpp)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills)
- [Whisper Docs](artifact/references/WHISPER_DOCS.md)
- [Available Models](artifact/references/AVAILABLE_MODELS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime outputs include TXT, SRT, and JSON transcript files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local transcript files and download Whisper model binaries into assets/models or configured model directories.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config.json; released 2026-03-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
