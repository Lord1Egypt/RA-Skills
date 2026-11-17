## Description:

Free local speech-to-text transcription using OpenAI Whisper for audio and video files without cloud API costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickylin](https://clawhub.ai/user/nickylin)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agent users use this skill to transcribe local audio or video into text, JSON, SRT, or VTT outputs. It is useful for voice memos, subtitles, multilingual transcription, and local STT workflows that avoid cloud API costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency and Whisper model setup may download packages or model files during installation or first use.

Mitigation: Install in an isolated Python environment, pin dependency versions where practical, and review downloads according to local policy.

Risk: System-wide package installation or demo execution with elevated privileges can expand local execution risk.

Mitigation: Avoid elevated privileges unless system-wide ffmpeg installation is intentionally required.

Risk: Transcription outputs can contain sensitive content from local audio or video files.

Mitigation: Use trusted local inputs and review generated text, JSON, SRT, or VTT before sharing or publishing.

## Reference(s):

- [OpenAI Whisper](https://github.com/openai/whisper)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; transcription outputs may be JSON, plain text, SRT, or VTT.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports selectable Whisper model size, optional language code, and local file input.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
