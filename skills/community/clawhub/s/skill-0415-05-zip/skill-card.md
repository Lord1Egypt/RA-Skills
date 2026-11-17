## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to summarize web pages, local files, PDFs, images, audio, and YouTube links from an agent workflow through the summarize CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and using the skill depends on a third-party Homebrew tap and summarize CLI.

Mitigation: Confirm you trust the Homebrew tap and summarize CLI publisher before installation.

Risk: Content submitted for summarization may be sent to model providers or optional fallback services.

Mitigation: Avoid summarizing sensitive, private, regulated, or confidential files unless the configured providers are approved; disable Firecrawl or Apify fallbacks when they are not needed.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/skill-0415-05-zip)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples; the summarize CLI can emit text or JSON summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the summarize CLI and model provider API keys; optional Firecrawl and Apify fallbacks may be used when configured.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
