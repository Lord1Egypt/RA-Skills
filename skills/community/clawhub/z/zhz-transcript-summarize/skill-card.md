## Description:

Transcribes local audio and video, then creates focused summaries that can be regenerated from different angles using a cached transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjbook](https://clawhub.ai/user/bjbook)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can transcribe a local recording and create a focused summary, meeting notes, analysis, or subtitles. They can rerun summarization with a different focus without repeating transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes undeclared file and shell capabilities and subprocess use; its analysis was partial.

Mitigation: Review requested file and shell access before execution, and provide only the intended local media files.

## Reference(s):

- [Publisher homepage](http://openclaw.bjbook.net/)
- [ClawHub skill release](https://clawhub.ai/bjbook/skills/zhz-transcript-summarize)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, Subtitle files]

**Output Format:** [Transcript and summary files in plain text, JSON, Markdown, HTML, SRT, or VTT formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary focus, audience, format, length, and language are configurable; transcripts are cached by content.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
