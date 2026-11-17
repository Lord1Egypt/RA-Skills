## Description:

Fetches transcripts from YouTube videos, public podcast episodes including Xiaoyuzhou, other public media links, and local audio or video files, preferring existing captions before using AudioFlow ASR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niuzb](https://clawhub.ai/user/niuzb)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to obtain transcripts from public media links or local media files, then optionally summarize, answer questions, or extract information grounded in the transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted public media links may cause downloader requests from the user's machine to internal network targets.

Mitigation: Use the skill only with trusted media links, keep review-before-install posture, and enforce the documented rejection of non-public, private, login-required, and network-local URLs.

Risk: Remote ASR sends local or downloaded media plus metadata to AudioFlow and a signed HTTPS object-storage URL.

Mitigation: Require explicit per-run approval before adding remote-ASR consent, disclose what will be uploaded, and stop without upload when the user declines or does not answer.

Risk: The skill may store an AudioFlow API token locally or use an AUDIOFLOW_TOKEN environment variable.

Mitigation: Prefer the documented token handling path, avoid echoing or logging tokens, and use the configured credential directory only for user-approved AudioFlow credentials.

Risk: The skill can optionally cache a managed yt-dlp executable.

Mitigation: Download and cache the pinned, SHA-256-verified yt-dlp release only after separate explicit user approval.

## Reference(s):

- [Transcribe Media ClawHub page](https://clawhub.ai/niuzb/skills/transcribe-media)
- [Xiaoyuzhou episode handling reference](references/xiaoyuzhou.md)
- [AudioFlow ASR service endpoint](https://asr.audioflow123.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text transcript or Markdown response; script output may be text or JSON containing transcript text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript-only requests are returned verbatim; summaries, answers, and extraction outputs are grounded in the obtained transcript.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
