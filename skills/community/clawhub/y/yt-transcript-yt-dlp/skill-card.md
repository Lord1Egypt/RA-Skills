## Description:

Extracts YouTube video transcripts from existing captions using yt-dlp, with optional timestamps and local SQLite caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mpbshhx](https://clawhub.ai/user/mpbshhx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content workflows use this skill to turn YouTube URLs or video IDs into transcript JSON or plain text for summarization, search, review, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube video identifiers are sent to YouTube when transcripts are requested.

Mitigation: Use the skill only for videos where sharing the video identifier with YouTube is acceptable.

Risk: Optional cookies can expose sensitive YouTube or Google session information.

Mitigation: Provide cookies only when required for restricted videos, keep them under ~/.config/yt-transcript/, and avoid using broad browser session cookies.

Risk: Transcript text is stored in a local SQLite cache and may contain private or sensitive content.

Mitigation: Use a controlled cache path and clear the transcript cache after processing sensitive videos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mpbshhx/skills/yt-transcript-yt-dlp)
- [Publisher profile](https://clawhub.ai/user/mpbshhx)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON transcript objects or newline-separated plain text, with optional timestamp fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and yt-dlp; accepts a YouTube URL or video ID, optional language, timestamp, cache, and cookies settings.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
