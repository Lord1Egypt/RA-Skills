## Description:

Helps agents build and troubleshoot SenseAudio speech recognition integrations across HTTP transcription, realtime WebSocket ASR, audio quality analysis, and recognition record queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select SenseAudio ASR modes and models, construct authenticated API requests, validate model and parameter compatibility, and handle transcription, streaming, analysis, and records responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic speech-to-text or audio tasks could be routed to SenseAudio without the user clearly choosing that provider.

Mitigation: Confirm the user selected SenseAudio or already has SenseAudio in scope before sending audio or recognition requests.

Risk: Uploaded audio, transcripts, returned audio URLs, session IDs, trace IDs, recognition records, and API keys may contain sensitive operational or personal data.

Mitigation: Use SENSEAUDIO_API_KEY from the environment, send credentials only in the Authorization header, and avoid placing sensitive values in queries, logs, saved examples, or user-visible output.

Risk: Unsupported model and parameter combinations can produce failed or misleading ASR requests.

Mitigation: Check model feature compatibility before sending requests, including WebSocket, translation, diarization, timestamp, language, punctuation, and ITN constraints.

## Reference(s):

- [ASR Reference](references/asr.md)
- [SenseAudio Homepage](https://senseaudio.cn)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with API examples, code snippets, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SenseAudio request construction and parsing guidance; should avoid exposing API keys, transcripts, audio URLs, session IDs, and trace IDs.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
