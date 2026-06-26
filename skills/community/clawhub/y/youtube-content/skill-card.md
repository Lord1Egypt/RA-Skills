## Description: <br>
Transcribes and extracts YouTube video content using transcript-first routing, Whisper fallback, batch processing, and structured notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[milesnee](https://clawhub.ai/user/milesnee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content workflows use this skill to turn YouTube links into transcripts, summaries, structured notes, chapters, threads, blog posts, or quotes. It prioritizes available subtitles and falls back to Whisper transcription when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The yt-dlp fallback can read Chrome-stored YouTube session cookies. <br>
Mitigation: Prefer the transcript API path or unauthenticated yt-dlp first, and use browser-cookie access only with explicit user awareness for videos that require login. <br>
Risk: Whisper transcription can produce empty or truncated output without a clear failure signal. <br>
Mitigation: Check that generated transcript files are non-empty and verify coverage against the audio duration before using the transcript. <br>


## Reference(s): <br>
- [Output Format Reference](references/output-formats.md) <br>
- [Whisper Transcription Reference](references/whisper-transcription.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON transcript data, timestamped text, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default outputs are structured notes; alternate formats include summaries, chapters, chapter summaries, social threads, blog posts, and timestamped quotes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
