## Description:

TinkerClaw YouTube lets agents fetch YouTube transcripts, download media with yt-dlp, and search or inspect YouTube data through an opt-in read-only Google OAuth flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent collect YouTube transcripts, search and inspect video or channel data, read comments and account-linked YouTube data, and download video or audio for local analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account-linked commands can read YouTube account data through a local Google OAuth grant and store a read-only token on disk.

Mitigation: Use a dedicated Google OAuth client, review the consent prompt, set YOUTUBE_SKILL_NO_ACCOUNT=1 for transcript/download-only use, and run logout plus revoke the grant in the Google account when finished.

Risk: Download commands can write media files to the chosen output folder or current directory.

Mitigation: Use an explicit output directory for downloads, or set YOUTUBE_SKILL_NO_DOWNLOAD=1 when media writes are not desired.

Risk: The skill may reuse an existing gogcli OAuth client if no YouTube skill credentials file is present.

Mitigation: Place a dedicated client at ~/.config/youtube-skill/credentials.json when stronger separation from other Google tooling is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/youtube-ultimate)
- [Publisher profile](https://clawhub.ai/user/globalcaos)
- [YouTube read-only OAuth scope](https://www.googleapis.com/auth/youtube.readonly)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text or JSON output, with local media files produced for download commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript, search, comments, channel, playlist, subscription, account, logout, video download, and audio download command outputs.]

## Skill Version(s):

4.3.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
