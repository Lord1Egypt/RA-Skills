## Description:

Extract and analyze YouTube video transcripts without watching the video. Use when users request video summaries, ask to "analyze this YouTube video", want transcripts extracted, or need to understand video content quickly. Handles any YouTube URL and provides cleaned transcripts plus AI analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xanderrey](https://clawhub.ai/user/xanderrey)

### License/Terms of Use:


## Use Case:

Developers, researchers, content reviewers, and other users can use this skill to extract YouTube captions and turn video content into concise summaries, key takeaways, notable quotes, and action items without watching the full video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extraction script can automatically download and run an unverified yt-dlp executable from GitHub under the user's account.

Mitigation: Review the script before use and prefer preinstalling yt-dlp from a trusted source or pinning and verifying the downloaded binary before execution.

Risk: Videos without captions, private or restricted videos, network failures, or age restrictions can prevent transcript extraction.

Mitigation: Disclose extraction failures clearly and use only basic video information as a fallback when captions are unavailable.

Risk: Auto-generated transcripts can contain repeated phrases, transcription errors, missing punctuation, or incorrect technical terms.

Mitigation: Treat quotes and technical claims as reviewable output and cross-check important details before relying on them.

## Reference(s):

- [YouTube Transcript Analysis Patterns](references/analysis-patterns.md)
- [yt-dlp release download](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp)
- [ClawHub skill page](https://clawhub.ai/xanderrey/skills/youtube-transcript-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with optional plain-text transcript files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript quality depends on available captions and may require review for auto-generated transcription errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
