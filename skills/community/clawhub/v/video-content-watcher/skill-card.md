## Description:

Extract core content and generate structured analysis reports from YouTube, Bilibili, or local video files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklinyung](https://clawhub.ai/user/franklinyung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content analysts use this skill to extract transcripts from online or local videos and produce structured Markdown summaries, key takeaways, viewpoints, pros and cons, and audience guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill imports implementation code from a hard-coded local video-reader project path that is not bundled with the release.

Mitigation: Install only when that local project is trusted, reviewed, and present at the expected path.

Risk: Video, transcript, or raw text content may be sent to third-party MiniMax or OpenAI APIs depending on configuration.

Mitigation: Avoid private, regulated, or confidential videos unless local transcription is confirmed and third-party data handling is acceptable.

## Reference(s):

- [Video Reader Technical Reference](artifact/references/api_details.md)
- [MiniMax API endpoint](https://api.minimaxi.com/v1)
- [ClawHub skill page](https://clawhub.ai/franklinyung/skills/video-content-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires video source input or raw text and configured MiniMax and optional Whisper credentials.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
