## Description:

Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bestrong1608-eng](https://clawhub.ai/user/bestrong1608-eng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to invoke the summarize CLI for concise summaries of URLs, local files, and YouTube links. It is useful when an agent needs a repeatable command-line path for text summaries, extraction-only output, or machine-readable JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Summarized URLs, local files, images, audio, or YouTube content may be sent to external model providers or optional extraction services.

Mitigation: Use only approved providers for sensitive data, avoid confidential inputs unless the provider is authorized, and prefer scoped API keys.

Risk: The required summarize CLI is installed from a third-party Homebrew tap.

Mitigation: Review the Homebrew formula and source before installing in higher-trust environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bestrong1608-eng/skills/summarize-backup)
- [Summarize homepage](https://summarize.sh)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI output may be plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports selectable summary lengths, maximum output token limits, extraction-only mode, optional Firecrawl extraction, optional Apify YouTube fallback, and provider API key configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
