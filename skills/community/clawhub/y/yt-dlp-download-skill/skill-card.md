## Description:

yt-dlp-powered downloader for YouTube, Bilibili, X (Twitter), TikTok/Douyin, and more. Given a video URL, download video (720p/1080p/best), extract MP3/audio-only, fetch subtitles (specify languages), and optionally download playlists; auto-merges audio/video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatelei](https://clawhub.ai/user/fatelei)

### License/Terms of Use:

Apache License

## Use Case:

People who use an AI agent to save user-selected online video or audio can request a download, choose quality or audio extraction, and optionally request subtitles or a playlist. Downloads use the requested service and media hosts and are saved to a chosen destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subtitle mode downloads all available languages, although the skill description suggests languages can be specified.

Mitigation: Tell the user that all available subtitle languages will be fetched and review the resulting files for unwanted languages.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fatelei/skills/yt-dlp-download-skill)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [Downloaded video, audio, or subtitle files with concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quality, audio extraction, subtitles, playlist inclusion, and destination follow the request.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
