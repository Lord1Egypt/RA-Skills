## Description:

Downloads Xiaohongshu (小红书/RedNote) videos and can create resource packs containing video, audio, subtitles, transcripts, and AI summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smile7up](https://clawhub.ai/user/smile7up)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to download Xiaohongshu video content, extract audio and subtitles, create transcripts, and optionally prepare a Markdown summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser cookie extraction can access local browser session data when enabled.

Mitigation: Review before installing, use --browser none when possible, and prefer a sandboxed environment when cookie-based authentication is needed.

Risk: Untrusted links, configurable output paths, and private videos can create privacy or file-placement concerns.

Mitigation: Only process links you trust, avoid summarizing private or sensitive videos, and confirm the intended output directory before running downloads.

Risk: Transcription fallback may install or execute runtime dependencies.

Mitigation: Use a controlled environment and review dependency behavior before enabling the Whisper transcription fallback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smile7up/skills/xiaohongshu-downloader)
- [Summary prompt template](reference/summary-prompt.md)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [uv](https://docs.astral.sh/uv/)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, Shell commands, Guidance]

**Output Format:** [Downloaded media files, transcript text, optional Markdown summary, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to the configured output directory; summary mode can add metadata and a generated summary.md file.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
