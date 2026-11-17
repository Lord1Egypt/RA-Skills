## Description:

yt-dlp. Use when the user wants to download, extract audio, pull subtitles, clip, or archive a YouTube or other streaming-site URL, or when yt-dlp hits 403, bot-check, or only-360p. Not for local-file edit/transcode, watch/summarize without saving, search, or generic downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to save streaming-site media, extract audio, pull subtitles, cut clips, or archive bounded playlists and channels with yt-dlp while preserving clear stopping points for rights, scope, authentication, and missing local tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide downloads of media the user may not have rights to save.

Mitigation: Stop when rights are unclear and proceed only for media the user confirms they have permission to save.

Risk: Browser cookies, cookie files, PO tokens, or credential-bearing headers can expose secrets through logs, command history, process listings, or transcripts.

Mitigation: Ask before cookie use, prefer approved browser-cookie access, do not inspect or print cookie contents, and stop when a workaround would require exposing token material.

Risk: Unbounded playlist or channel downloads can expand scope unexpectedly.

Mitigation: Require confirmation of the playlist or channel range or archive scope, and use a download archive for reruns.

Risk: Missing or stale local tools can produce failed, incomplete, or misleading media outputs.

Mitigation: Verify yt-dlp and ffmpeg before jobs that need them, update yt-dlp before extractor retries, and report explicit blockers when required tools are unavailable.

## Reference(s):

- [YouTube auth and extractor failure late route](references/youtube-auth.md)
- [yt-dlp upstream project](https://github.com/yt-dlp/yt-dlp)
- [ClawHub skill page](https://clawhub.ai/tmchow/skills/yt-dlp-cli)
- [Publisher profile](https://clawhub.ai/user/tmchow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash command examples and concise blocker reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated local media file paths, sizes, media identity, verification performed, stderr, or a named blocker.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
