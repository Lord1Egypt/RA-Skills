## Description:

Download audio (MP3) and video (MP4) files from YouTube URLs. Use when users want to convert YouTube videos to files, extract music/songs, download videos for offline viewing, save educational content, or process playlists. Handles single videos, playlists, and batch downloads with quality options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xanderrey](https://clawhub.ai/user/xanderrey)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to download YouTube videos, extract MP3 audio, and process playlists or URL batches with selectable output quality and file organization options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can automatically download and run yt-dlp and ffmpeg binaries from third-party GitHub release URLs without version pinning or checksum verification.

Mitigation: Install yt-dlp and ffmpeg from trusted sources before using the skill, or require pinned versions with verified checksums or signatures and explicit approval before downloading executables.

Risk: The skill downloads media from user-provided YouTube URLs, which may involve copyrighted content or platform terms of service constraints.

Mitigation: Use the skill only for content the user is authorized to download and keep redistribution and reuse decisions outside the automated workflow.

## Reference(s):

- [YouTube Download Patterns & Best Practices](references/download-patterns.md)
- [ClawHub skill page](https://clawhub.ai/xanderrey/skills/youtube-media-downloader)
- [Publisher profile](https://clawhub.ai/user/xanderrey)
- [yt-dlp release binary URL used by scripts](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp)
- [FFmpeg release archive URL used by scripts](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; downloaded MP3 or MP4 media files from the scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single URLs, playlists, URL files, output directory selection, filename selection, playlist ranges, max-download limits, and video quality choices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
