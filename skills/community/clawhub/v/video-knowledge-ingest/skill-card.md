## Description:

Ingest and summarize cross-platform videos into a local knowledge base by fetching subtitles when available, falling back to local media download and Whisper transcription when needed, and saving transcript, summary, and metadata files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[exsusiai](https://clawhub.ai/user/exsusiai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to ingest YouTube, Bilibili, Xiaohongshu, local media, and local subtitle/text sources into reusable local video notes. It supports subtitle-first extraction, Whisper fallback transcription, Codex-backed summarization, and troubleshooting for common fetch, transcription, and summarization failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can download remote media and store transcripts, summaries, metadata, and index entries locally.

Mitigation: Use it only for inputs whose download, processing, and local retention are acceptable; use a custom --kb-root or manually remove stored outputs when needed.

Risk: Transcripts are sent to the configured Codex-backed summarizer.

Mitigation: Avoid private, regulated, or confidential video content unless that summarization path is approved for the data.

Risk: External platform access, local transcription dependencies, or summarizer authentication can fail.

Mitigation: Follow the bundled troubleshooting guidance for YouTube, Bilibili, Xiaohongshu, ffmpeg, Whisper, yt-dlp, summarize, and Codex authentication issues.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/exsusiai/skills/video-knowledge-ingest)
- [Toolchain Reference](references/toolchain.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON stdout plus local Markdown, text, and metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists source metadata, transcript.txt, summary.md, record.json, downloaded media or subtitles when used, Whisper artifacts when used, and an append-only index entry.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
