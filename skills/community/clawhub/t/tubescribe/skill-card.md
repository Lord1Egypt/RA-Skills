## Description: <br>
YouTube video summarizer with speaker detection, formatted documents, and audio output. Works out of the box with macOS built-in TTS. Optional recommended tools (pandoc, ffmpeg, mlx-audio) enhance quality. Requires internet for YouTube access. No paid APIs or subscriptions. Use when user sends a YouTube URL or asks to summarize/transcribe a YouTube video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matusvojtek](https://clawhub.ai/user/matusvojtek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use TubeScribe to turn YouTube URLs into transcript-based summaries, formatted documents, speaker labels, timestamped quotes, comment highlights, and optional audio summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A YouTube URL can trigger background processing that fetches captions or comments, writes local files, and generates audio. <br>
Mitigation: Review the URL before processing, avoid private or sensitive videos, and require user confirmation before starting automated background work when appropriate. <br>
Risk: Transcript and comment text may be exposed to the active agent or model environment during summarization. <br>
Mitigation: Do not use the skill with confidential video content, and review generated summaries and documents before sharing them. <br>
Risk: Optional setup and TTS tooling may rely on local user-writable tool paths and downloads. <br>
Mitigation: Review setup.py before accepting optional downloads, prefer trusted package sources, and skip optional installs when the built-in workflow is sufficient. <br>


## Reference(s): <br>
- [TubeScribe on ClawHub](https://clawhub.ai/matusvojtek/tubescribe) <br>
- [Kokoro TTS](https://github.com/hexgrad/kokoro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts may include DOCX, HTML, Markdown, MP3, or WAV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local outputs under ~/Documents/TubeScribe by default; requires internet for YouTube fetching and can use local TTS tooling when available.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release metadata and CHANGELOG, released 2026-02-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
