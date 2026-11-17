## Description:

Automatically generates subtitles for video and audio files, with multilingual recognition, translation, speaker separation, and optional subtitle burn-in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwerty0205](https://clawhub.ai/user/qwerty0205)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, media teams, and agents use this skill to transcribe video or audio into subtitle and transcript files, optionally translate captions, distinguish speakers, and produce videos with burned-in subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio or video content is uploaded to SenseAudio for cloud transcription.

Mitigation: Use the skill only with media that is approved for SenseAudio processing, and avoid confidential or regulated recordings unless that service is approved for the use case.

Risk: API keys may be exposed by commands that print SENSEAUDIO_API_KEY or by passing the key directly as a command-line argument.

Mitigation: Do not run commands that echo the API key; prefer a protected environment variable or secret store and avoid the --senseaudio-api-key argument.

Risk: Generated transcripts, subtitle files, detailed JSON, and burned-in videos may persist sensitive content locally.

Mitigation: Review and manage the output directory after each run, and remove sensitive generated files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qwerty0205/skills/video-subtitle-skill)
- [Publisher profile](https://clawhub.ai/user/qwerty0205)
- [SenseAudio](https://senseaudio.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated subtitle, transcript, JSON, and optional video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SRT, VTT, TXT, detailed JSON, extracted audio, and optionally burned-in video outputs in a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
