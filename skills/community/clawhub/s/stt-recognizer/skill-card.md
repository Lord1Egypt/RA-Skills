## Description:

Speech-to-text skill that records microphone audio and transcribes audio files locally with Whisper/faster-whisper or through an OpenAI-compatible API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can record speech or submit audio files for transcription, choosing local Whisper inference or an OpenAI-compatible API based on privacy, hardware, and connectivity needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can record microphone audio and upload audio to an OpenAI-compatible API, which may expose sensitive speech.

Mitigation: Get explicit user consent, prefer local transcription for sensitive audio, use only trusted HTTPS endpoints or intentional localhost endpoints, and delete recordings and transcripts when no longer needed.

Risk: Dependency installation guidance uses broad version ranges and includes --break-system-packages.

Mitigation: Install in a virtual environment and pin or lock dependencies before operational use.

Risk: API keys can be passed through command-line options and may be exposed through shell history or process listings.

Mitigation: Avoid passing API keys on the command line; use a secret manager or protected environment configuration and rotate keys if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moroiser/skills/stt-recognizer)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; runtime outputs include WAV recordings and text transcription files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcriptions may be saved as txt, srt, or vtt files; recorded audio and transcripts can remain on disk until deleted.]

## Skill Version(s):

1.0.8 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
