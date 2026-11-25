## Description:

Transcribe project speech for understanding, editing, or dubbing without automatically creating visible captions. Use for transcript-only, speech analysis, translation preparation, and dialogue references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to transcribe selected project audio for understanding, editing, translation preparation, or dubbing. It distinguishes private reference transcripts from visible captions and can reuse saved transcripts when the source and trim still match.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud transcription, including speaker detection, may send project audio to a remote service.

Mitigation: Use local transcription for sensitive audio when it meets the task needs, or confirm that remote processing is acceptable before choosing cloud mode.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/prosamik/skills/subclip-transcription)
- [Publisher profile: prosamik](https://clawhub.ai/user/prosamik)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Timed transcript data with a readable Markdown transcript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcripts are scoped to the selected audio or media item; visible captions are created only when requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
