## Description:

Transcribes Brazilian Portuguese audio files to text using OpenAI Whisper, with support for multiple audio formats and timestamped segments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bohnwuks](https://clawhub.ai/user/bohnwuks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to convert inbound voice notes and audio files into structured transcripts for review or downstream automation. It supports single-file transcription, batch processing, and directory monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbound audio files and generated transcript JSON may contain sensitive speech content.

Mitigation: Run the skill in a controlled local environment and treat both source audio and transcript outputs as sensitive files.

Risk: Processed audio files are moved into output subdirectories after transcription.

Mitigation: Use dedicated input and output directories and confirm retention expectations before batch or watch-mode processing.

Risk: Audio and ML dependencies are unpinned and may change across installations.

Mitigation: Review or pin dependency versions, especially torch and Whisper-related packages, before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bohnwuks/skills/stt)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON transcript files and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript JSON includes file metadata, processing metadata, recognized text, and timestamped segments when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
