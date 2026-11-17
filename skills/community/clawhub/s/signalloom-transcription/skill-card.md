## Description:

Transcribes audio and video files using the Signal Loom AI API and supports common media formats such as MP3, WAV, M4A, MP4, and MOV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avale-slai](https://clawhub.ai/user/avale-slai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to turn meeting recordings, podcasts, videos, and other spoken media into searchable transcripts, subtitle files, or structured transcript data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package does not include the actual transcribe executable required by its metadata.

Mitigation: Confirm the transcribe binary is supplied and review installation contents before relying on the skill.

Risk: The installer makes a persistent change to the user's zsh startup file.

Mitigation: Review install.sh before execution and apply PATH changes manually when they match local policy.

Risk: The installer sends an install analytics request to Signal Loom, and the evidence says the local-only privacy claim is not verified.

Mitigation: Treat install telemetry and possible media or metadata upload as external communication until the publisher documents the behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avale-slai/skills/signalloom-transcription)
- [Publisher profile](https://clawhub.ai/user/avale-slai)
- [Signal Loom API key signup](https://signalloomai.com/signup)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [JSON, SRT/VTT subtitle files, and plain text transcripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON output may include timestamped words, confidence scores, and speaker diarization when supported.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact package.json is 1.0.1 and install.sh is 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
