## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to ask an agent to summarize web pages, local files, PDFs, images, audio, and YouTube links via the summarize CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The summarize CLI and its Homebrew tap are third-party dependencies.

Mitigation: Install only after confirming that the CLI and tap are trusted for the intended environment.

Risk: Summarized files, URLs, and media may be sent to selected model providers or optional fallback services.

Mitigation: Avoid sensitive, regulated, or private content unless the selected provider and fallback services are approved for that data.

Risk: The skill requires API credentials for chosen model providers and optional services.

Mitigation: Use scoped credentials, store them in environment variables or approved secret management, and rotate them according to local policy.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/test-0313-skill)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from the summarize CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports length controls, maximum output token settings, extract-only mode, machine-readable JSON, provider API keys, and optional Firecrawl or Apify fallbacks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
