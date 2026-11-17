## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to invoke the summarize CLI for concise summaries of URLs, local files, PDFs, images, audio, and YouTube links while selecting AI providers and optional extraction fallbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill depends on a Homebrew tap and the summarize CLI.

Mitigation: Confirm the Homebrew tap and summarize CLI are trusted before installation.

Risk: Summarized URLs or local files may be sent to the selected AI provider, and to Firecrawl or Apify when fallback extraction is enabled.

Mitigation: Do not summarize sensitive content unless the configured providers and optional extraction services are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/summarize-dudutest)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)
- [Summarize homepage](https://summarize.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce machine-readable JSON when the summarize CLI is used with --json.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
