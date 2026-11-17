## Description:

Subtitle extractor for Bilibili, YouTube, Xiaohongshu, Douyin, and local files. Extracts native subtitles or Whisper transcription in original format. Agent handles dependency checking, file naming, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poltawa](https://clawhub.ai/user/poltawa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract native subtitles or Whisper transcripts from supported video platforms and local media. The skill returns a subtitle file path with title, author, and platform metadata so the agent can save or process the transcript according to the user's request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles platform session cookies for some subtitle extraction flows.

Mitigation: Use narrowly scoped cookie exports and avoid using cookies with untrusted URLs.

Risk: Downloaded audio and generated transcript files may remain in the system temporary directory.

Mitigation: Review and remove temporary audio or transcript files after use when they may contain sensitive content.

Risk: Security evidence marks the release as suspicious pending review.

Mitigation: Review the skill before installing and confirm the cookie-handling and temporary-file behavior is acceptable for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/poltawa/skills/subtitle-extractor)
- [Publisher profile](https://clawhub.ai/user/poltawa)
- [ffmpeg downloads](https://ffmpeg.org/download.html)
- [Cookie Editor](https://cookieeditor.org/)
- [ModelScope faster-whisper base files](https://modelscope.cn/models/pkufool/faster-whisper-base/files)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing script calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces subtitle file paths and metadata; subtitle content may be SRT or VTT.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
