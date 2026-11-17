## Description:

Transcribes WAV, MP3, M4A, and FLAC audio to timestamped text using SenseVoice-Small with FSMN-VAD, supporting single-file and batch daylog workflows with VAD-anchored segment timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylongw](https://clawhub.ai/user/ylongw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to transcribe speech recordings into timestamped text files, including batch processing of daylog audio grouped by recording date. It is especially oriented toward Mandarin/Chinese audio workflows that need VAD-anchored timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that optional flags can delete or overwrite user-controlled paths.

Mitigation: Run in a constrained working directory, preview with dry-run where possible, avoid --force-dates unless date arguments are trusted, and avoid pointing --progress-file at existing important files.

Risk: The security review notes that the Discord webhook option can send filenames, dates, status, and error details to an arbitrary endpoint.

Mitigation: Use --discord-webhook only with trusted endpoints and only when sending those job details is acceptable.

Risk: The security guidance recommends caution around dependency and model downloads.

Mitigation: Prefer pinned dependencies and a sandboxed environment for model downloads and transcription runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylongw/skills/sensevoice-transcribe)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Timestamped transcript text files, progress JSON when configured, and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcripts use one timestamped segment per line, generally around 15-second granularity when VAD timestamps are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
