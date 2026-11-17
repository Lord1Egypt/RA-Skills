## Description:

A CLI wrapper for yt-dlp that helps agents download videos, playlists, and audio while supporting format selection, quality controls, metadata embedding, and cookie authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for yt-dlp download commands and media-archiving workflows for videos, playlists, channels, audio extraction, and authenticated downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing yt-dlp or ffmpeg from untrusted sources can expose users to tampered binaries or unsafe install scripts.

Mitigation: Install only from trusted yt-dlp and ffmpeg sources, prefer pinned or package-managed installs, and verify downloaded artifacts before use.

Risk: Browser-cookie options can expose authenticated sessions or broaden access beyond the intended site.

Mitigation: Use cookie options only on trusted machines and prefer manually exported, site-scoped cookies.txt files for agent workflows.

Risk: The skill can download media from third-party sites, which may create copyright, terms-of-service, or data-handling obligations.

Mitigation: Use the generated commands only for content the user is authorized to download and retain.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1999azzar/skills/yt-dlp)
- [yt-dlp Comprehensive Usage Guide](references/guide.md)
- [yt-dlp Usage Guide](references/usage.md)
- [yt-dlp Latest Release Binary](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in downloaded media files when the generated shell commands are executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
