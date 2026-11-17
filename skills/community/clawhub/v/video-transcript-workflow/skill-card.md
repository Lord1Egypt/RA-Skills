## Description:

Transcribes video or audio with Whisper, refines the transcript, extracts highlights, and drafts Markdown posts for Zhihu, WeChat, and Xiaohongshu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artminding](https://clawhub.ai/user/artminding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and content teams use this skill to turn video or audio into timestamped transcripts, edited long-form notes, and platform-specific publication drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript-derived terms may be used for automatic web lookups, which can expose sensitive recording context.

Mitigation: For confidential recordings, run in local-only mode and skip web_search or web_fetch during knowledge enrichment.

Risk: User preferences may be saved for future runs without clear consent controls.

Mitigation: Ask before saving preferences, or disable persistent memory updates for users who do not want reuse across sessions.

Risk: Generated transcripts and publication drafts can contain transcription errors, unsupported corrections, or unsuitable publishing claims.

Mitigation: Review generated files, low-confidence correction notes, and platform drafts before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/artminding/skills/video-transcript-workflow)
- [OpenAI Whisper](https://github.com/openai/whisper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown and timestamped text files, with inline shell commands when transcription scripts are invoked]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates transcript files, optimized transcript drafts, platform-specific article drafts, correction review tables, and publishing guidance.]

## Skill Version(s):

2.2.0 (source: server release metadata, package.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
