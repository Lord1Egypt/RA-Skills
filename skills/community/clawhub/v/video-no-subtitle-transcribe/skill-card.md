## Description:

Fallback transcription for videos without subtitles: it downloads audio with yt-dlp, transcribes locally with faster-whisper, and produces a full timestamped transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bccbok](https://clawhub.ai/user/bccbok)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and other external users use this skill when subtitle-based video workflows fail or a local audio/video file needs timestamped speech transcription for later review or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download a 483MB speech model into the user's home directory.

Mitigation: Tell users about the model download before first use and allow enough disk space and time for the download to complete.

Risk: yt-dlp fetches media from URLs provided by the user and proxy settings may be read automatically.

Mitigation: Use only URLs the user is authorized to process and avoid authenticated proxy URLs that could be exposed in local process listings.

Risk: The optional iiilab browser fallback sends the source YouTube URL to a third-party service.

Mitigation: Use the browser fallback only after yt-dlp fails, and do not use it for private, unlisted, sensitive, or client-owned videos unless the user explicitly approves.

## Reference(s):

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [ModelScope faster-whisper-small model file](https://modelscope.cn/models/Systran/faster-whisper-small/resolve/master/model.bin)
- [bilibili-youtube-watcher companion skill](https://clawhub.ai/donnycui/skills/bilibili-youtube-watcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Timestamped transcript text with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript lines include segment start and end times; output language is controlled by the --lang parameter.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
