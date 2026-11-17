## Description:

Voice-to-text transcription toolkit supporting Whisper and Vosk engines, batch processing, audio conversion, and SRT/VTT subtitle export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe local audio files, process batches of recordings, convert audio to WAV, inspect audio metadata, and export transcript segments as SRT or WebVTT subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can return fabricated transcript text as a successful-looking result when Whisper or Vosk is unavailable.

Mitigation: For high-reliability workflows, remove the mock fallback or require the agent to check the returned note, model, and status before trusting transcript text.

Risk: The skill processes local audio files through Python speech libraries and ffmpeg.

Mitigation: Install and run it only in an isolated environment with pinned dependencies when handling sensitive or production audio.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/voice-transcriber-toolkit)
- [Publisher profile](https://clawhub.ai/user/kaiyuelv)
- [README](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime helpers return dictionaries, subtitle strings, and audio metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports WAV, MP3, M4A, FLAC, OGG, and WEBM inputs, Whisper or Vosk engines, batch transcription, ffmpeg-based conversion, and SRT/VTT subtitle export.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
