## Description:

Extract subtitles from YouTube or Bilibili, save the raw transcript, and generate a structured summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiapuyang](https://clawhub.ai/user/xiapuyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn YouTube or Bilibili videos into local Markdown transcripts and structured summaries. It is suited for reviewing video content, preserving subtitle text, and generating concise topic-oriented notes from short or long videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install or update yt-dlp.

Mitigation: Review the commands before use and prefer a release or local workflow that asks before installing or updating software.

Risk: For Bilibili links, the skill can access Chrome or keychain cookies and store a reusable cookie file in the user's home directory.

Mitigation: Use only when cookie access is acceptable; prefer a temporary or user-supplied cookie file with restrictive permissions.

Risk: The skill depends on subtitles being available from the target video.

Mitigation: Expect the workflow to stop when no manual or auto-generated subtitles are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiapuyang/skills/youtube-subtitle-summary)
- [Publisher profile](https://clawhub.ai/user/xiapuyang)
- [Bilibili](https://www.bilibili.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown transcript and Markdown summary files with YAML frontmatter, plus shell command output during subtitle retrieval.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a raw transcript file and a companion summary file; long transcripts are summarized through chunked map-reduce notes before final synthesis.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
