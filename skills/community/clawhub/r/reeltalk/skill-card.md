## Description: <br>
Helper for processing shared video links: it downloads audio, creates a transcript, and produces a summary, with OCR fallback when speech is absent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ameshalexk](https://clawhub.ai/user/ameshalexk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to understand shared video links without watching them by generating metadata, transcripts, OCR text when needed, and a plain-English summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-supplied video URLs and related media from third-party services, including fxtwitter for X/Twitter links. <br>
Mitigation: Use only links appropriate for third-party retrieval, avoid sensitive private URLs, and review the generated commands before execution. <br>
Risk: The skill writes temporary media and transcript files under /tmp/reeltalk_* and uses the local Whisper cache. <br>
Mitigation: Run it in an environment where local temporary files are acceptable and clear /tmp/reeltalk_* after use when the content is sensitive. <br>
Risk: Video processing depends on local tools such as yt-dlp, whisper, tesseract, and ffmpeg and may be slow for longer videos. <br>
Mitigation: Confirm required binaries are installed and warn users before processing videos longer than five minutes. <br>


## Reference(s): <br>
- [ReelTalk on ClawHub](https://clawhub.ai/ameshalexk/reeltalk) <br>
- [Publisher profile](https://clawhub.ai/user/ameshalexk) <br>
- [fxtwitter API endpoint used for X/Twitter media lookup](https://api.fxtwitter.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text summary output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local temporary media, transcript, OCR, and metadata files under /tmp/reeltalk_work during execution.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
