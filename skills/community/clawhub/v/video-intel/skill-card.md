## Description:

Downloads videos and extracts transcripts, summaries, or metadata from YouTube, TikTok, Instagram, and X when a user shares a video URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nogara](https://clawhub.ai/user/nogara)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to fetch captions, transcribe audio when captions are unavailable, inspect video metadata, or download video and audio from supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that a crafted video title can reach unsafe shell execution in the bundled script.

Mitigation: Review before installing, use only trusted video URLs until shell filename handling is fixed, and avoid running the skill in privileged environments.

Risk: When captions are unavailable, downloaded audio may be sent to OpenAI for transcription if OPENAI_API_KEY is set.

Mitigation: Unset OPENAI_API_KEY or use a local transcription path when external audio transmission is not acceptable.

Risk: The setup guidance downloads yt-dlp from a latest-release URL.

Mitigation: Prefer a pinned and checksum-verified yt-dlp installation for repeatable deployments.

## Reference(s):

- [OpenAI Audio Transcriptions API](https://api.openai.com/v1/audio/transcriptions)
- [yt-dlp release download](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp)
- [ClawHub skill page](https://clawhub.ai/nogara/skills/video-intel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create cached caption, audio, or video files under /tmp/video-intel during execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
