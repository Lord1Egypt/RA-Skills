## Description:

Summarizes YouTube videos from supplied links by extracting transcripts through TranscriptAPI and producing concise, structured summaries with optional user instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chapati23](https://clawhub.ai/user/chapati23)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn YouTube links into concise summaries, key points, and notable quotes. It is useful for quickly reviewing video content when captions are available through TranscriptAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends YouTube video identifiers and transcript requests to TranscriptAPI.com and requires a stored TranscriptAPI key.

Mitigation: Use the skill only when that third-party data flow is acceptable, store the key through the documented environment variable or password-store workflow, and keep access scoped to trusted environments.

Risk: Summaries of adversarial, sensitive, or high-impact video content may omit context or reproduce misleading claims from the transcript.

Mitigation: Review summaries before relying on them for sensitive decisions and compare important claims against the original video or transcript.

Risk: Python dependencies and external command behavior can change over time.

Mitigation: Use an isolated Python environment and pin dependency versions before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chapati23/skills/yt-summary)
- [TranscriptAPI](https://transcriptapi.com)
- [OpenClaw](https://openclaw.com)
- [YouTube oEmbed Endpoint](https://www.youtube.com/oembed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with optional status text and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are intended to stay under Telegram-friendly character limits; very long transcripts may be truncated before summarization.]

## Skill Version(s):

1.3.2 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
