## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[securecloudprojo](https://clawhub.ai/user/securecloudprojo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to summarize web pages, local documents, images, audio files, and YouTube links through the summarize CLI. It is useful when a workflow needs concise human-readable summaries or machine-readable JSON output from supported inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on a third-party Homebrew tap for the summarize CLI.

Mitigation: Install only when the Homebrew tap and package are trusted for the intended environment.

Risk: Summarization may send URLs, files, or extracted content to selected model or extraction providers.

Mitigation: Avoid submitting secrets, confidential documents, regulated data, or private URLs unless the selected providers are approved for that data.

Risk: Optional Firecrawl and Apify fallback extraction can introduce additional third-party data handling.

Mitigation: Use these integrations only with approved provider accounts and disable fallback extraction when it is not needed.

## Reference(s):

- [Summarize CLI homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/securecloudprojo/skills/summarize-garrison)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; summarize CLI output may be plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable summary length, model selection, token limits, JSON output, URL extraction, and optional YouTube or Firecrawl fallback extraction.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
