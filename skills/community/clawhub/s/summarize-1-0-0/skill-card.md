## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[garrisongg](https://clawhub.ai/user/garrisongg)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to summarize web URLs, local files, PDFs, images, audio, and YouTube links through the summarize CLI with configured AI providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on a third-party CLI from the steipete Homebrew tap.

Mitigation: Install only if you trust the Homebrew tap and the CLI package source.

Risk: Summarized content may be handled by configured model or extraction services.

Mitigation: Do not summarize secrets, confidential files, or private URLs unless that provider handling is acceptable.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/garrisongg/skills/summarize-1-0-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model selection, output length controls, JSON output, extraction-only mode, and optional service configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
