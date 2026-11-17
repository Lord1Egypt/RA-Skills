## Description:

Transcribes YouTube videos by extracting available captions first, then falling back to local Whisper transcription when captions are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iml885203](https://clawhub.ai/user/iml885203)

### License/Terms of Use:

MIT

## Use Case:

Users and developers use this skill to convert YouTube videos into transcripts for summarization, analysis, note-taking, or subtitle extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local command-line tools and optional Whisper Python packages.

Mitigation: Install dependencies in a dedicated virtual environment and prefer pinned package versions.

Risk: Whisper fallback may temporarily download YouTube audio and use significant local compute.

Mitigation: Use caption extraction when possible, confirm local storage and compute expectations before forcing Whisper, and remove generated transcript or audio artifacts when no longer needed.

## Reference(s):

- [YouTube Transcribe on ClawHub](https://clawhub.ai/iml885203/skills/youtube-transcribe)
- [Publisher profile: iml885203](https://clawhub.ai/user/iml885203)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, SRT, or VTT transcript output with Markdown usage guidance and bash command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write transcript output to stdout or a user-specified file; caption extraction is attempted before local Whisper fallback.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
