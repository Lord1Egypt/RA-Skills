## Description:

Automatically extracts subtitles, visual frames, OCR notes, timelines, and operational workflows from technical tutorial videos to generate reusable AI agent skill documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacob210](https://clawhub.ai/user/jacob210)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to convert technical tutorial videos into executable, reusable agent skills with transcripts, visual notes, OCR evidence, timelines, extracted principles, prompt templates, and validation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow defaults to using the user's Chrome browser session for video downloads.

Mitigation: Default to unauthenticated downloads and require explicit user consent before using browser cookies.

Risk: Video-derived subtitles, screen content, OCR text, and frames may be sent to unspecified remote models.

Mitigation: Disclose model providers and transmitted data, redact sensitive screen content, and require consent before remote-model use.

Risk: Generated skills may contain incorrect, misleading, or unsafe operational guidance.

Mitigation: Require human review, security scanning, and validation before installing or using any generated skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacob210/skills/video-2-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/jacob210)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown and JSON files with inline shell commands and structured evidence maps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates video metadata, raw and cleaned transcripts, visual notes, OCR notes, timeline data, extracted principles, a generated skill, an evidence map, and a debug report.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
