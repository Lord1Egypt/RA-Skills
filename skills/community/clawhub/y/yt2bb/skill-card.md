## Description:

Use when the user wants to repurpose a YouTube video for Bilibili, add bilingual (English-Chinese) subtitles to a video, or create hardcoded subtitle versions for Chinese platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and localization teams use this skill to turn YouTube videos or playlists into Bilibili-ready MP4 files with bilingual EN/ZH subtitles and Chinese upload metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask local tools to access a Chrome YouTube session and may leave exported cookies in cookies.txt.

Mitigation: Prefer unauthenticated yt-dlp downloads first; when cookies are needed, use a dedicated browser profile or temporary cookie file and delete cookies.txt after use.

Risk: The release requires local dependency and update-check commands that affect the user's execution environment.

Mitigation: Review the update-check and dependency-install commands before running them, and install only the required tools from trusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agents365-ai/skills/yt2bb)
- [Publisher profile](https://clawhub.ai/user/agents365-ai)
- [ffmpeg](https://ffmpeg.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Aegisub](https://aegisub.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, SRT/ASS subtitle files, MP4 video outputs, JSON-capable utility command results, and publish_info.md metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local media and subtitle files under a video-specific output directory; utility subcommands support --format json and dry-run checks where documented.]

## Skill Version(s):

2.5.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
