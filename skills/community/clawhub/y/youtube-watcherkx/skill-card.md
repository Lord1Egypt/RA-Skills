## Description:

Fetch and read transcripts from YouTube videos. Use when you need to summarize a video, answer questions about its content, or extract information from it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naliehu](https://clawhub.ai/user/naliehu)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to retrieve YouTube video transcripts, then summarize, search, or answer questions from the transcript text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on yt-dlp from the user's configured Homebrew or pip sources.

Mitigation: Install yt-dlp only from trusted package sources and keep it updated.

Risk: The inspected package references a transcript script that is not included in the artifact.

Mitigation: Confirm the transcript script is present and works before relying on the skill in an agent workflow.

Risk: Requests outside the stated YouTube transcript purpose may be triggered by broad video-analysis language.

Mitigation: Use the skill only for YouTube transcript retrieval and transcript-grounded summarization or question answering.

## Reference(s):

- [YouTube Watcher on ClawHub](https://clawhub.ai/naliehu/skills/youtube-watcherkx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and transcript-derived text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp and works only when the requested YouTube video has closed captions or auto-generated subtitles.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
