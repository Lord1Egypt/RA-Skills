## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmusjune](https://clawhub.ai/user/simmusjune)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install and run the summarize CLI for concise summaries of web pages, local documents, media, and YouTube links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents, URLs, and media may be processed by external model or extraction services.

Mitigation: Avoid confidential, regulated, or private inputs unless the selected provider and fallback services are approved for that data.

Risk: Installation depends on a third-party Homebrew tap and local summarize binary.

Mitigation: Install only from trusted sources and verify the configured CLI, model provider, and optional extraction services before use.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/simmusjune/skills/summarizer2)
- [Publisher profile](https://clawhub.ai/user/simmusjune)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI commands, configuration examples, and optional JSON output guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries can be controlled with length, max-output-token, extraction-only, JSON, Firecrawl, and YouTube fallback flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
