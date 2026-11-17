## Description:

Converts a video URL or local video file into a Chinese Markdown learning note by downloading and transcribing media, extracting timestamped frames, selecting key screenshots, and organizing section-by-section notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darknoah](https://clawhub.ai/user/darknoah)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, learners, and developers use this skill to turn authorized online or local videos into illustrated study notes with transcripts, selected screenshots, and review structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow downloads online media and writes video, transcript, frame, and note files locally.

Mitigation: Run it in a dedicated workspace and process only videos the user is authorized to access.

Risk: Using logged-in browser cookies for video downloads can expose sensitive session material.

Mitigation: Require explicit user approval before using browser cookies; prefer public URLs, manual downloads, dedicated browser profiles, or narrowly exported cookies.

Risk: Generated notes and screenshot interpretations can be incomplete or misleading if transcription or visual review misses context.

Mitigation: Review the transcript, selected frames, and final Markdown before relying on the notes.

## Reference(s):

- [Video Learning Notes Reference](references/api_reference.md)
- [ClawHub skill page](https://clawhub.ai/darknoah/skills/video-learning-notes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown learning note with local video, SRT transcript, timestamped image files, and JSON frame manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses relative paths, timestamped screenshots, and Chinese prose by default unless the user asks otherwise.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
