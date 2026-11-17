## Description:

Extract transcripts, video information, transcript previews, chapters, and key moments from public YouTube videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xraini](https://clawhub.ai/user/0xraini)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use this skill to inspect public YouTube videos by retrieving timestamped transcripts, summaries or transcript previews, chapters, and full analysis output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied YouTube URLs are passed through shell commands, which can allow local command injection.

Mitigation: Review before installing or running; replace shell command construction with argument-array execution such as execFileSync or spawnSync and apply stricter YouTube URL parsing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xraini/skills/yt-digest)
- [Publisher profile](https://clawhub.ai/user/0xraini)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [CLI text and Markdown-style sections with timestamps, metadata, chapters, transcript statistics, and transcript excerpts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp and access to public YouTube video transcripts; transcript output can be truncated with a character limit.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
