## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to summarize web URLs, PDFs, images, audio files, and YouTube links through the summarize CLI with configurable model and output settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and depends on an unpinned third-party CLI from a Homebrew tap.

Mitigation: Install only after reviewing and trusting the Homebrew tap and summarize CLI package source.

Risk: Files, URLs, media, and extracted content may be sent to selected model providers or optional extraction services.

Mitigation: Avoid using the skill with secrets, regulated data, private documents, or confidential URLs unless those providers and services are approved for that data.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-summarize)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or JSON summaries with optional inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable summary length, token limits, model selection, extraction-only mode, and optional fallback extraction services.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
