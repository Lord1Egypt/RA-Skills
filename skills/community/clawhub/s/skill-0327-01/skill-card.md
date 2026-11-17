## Description:

Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for concise CLI-driven guidance to summarize URLs, local documents, media files, and YouTube links with selectable model providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive files, private URLs, or extracted media content may be sent to the selected model provider or optional Firecrawl or Apify services.

Mitigation: Avoid using the skill on sensitive content unless those services are approved for the data, and enable only the provider or fallback service needed for the task.

Risk: Installing the summarize CLI from a Homebrew tap introduces supply-chain dependency risk.

Mitigation: Review the summarize CLI and Homebrew tap source before installation and keep the installed binary under normal dependency management.

Risk: Broadly configured provider API keys can expose unnecessary credentials to the CLI environment.

Mitigation: Provide only the API keys required for the selected model provider or fallback and avoid placing unnecessary credentials in shared shell or config files.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/skill-0327-01)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference provider API keys, optional extraction fallbacks, and CLI flags such as summary length, JSON output, extract-only mode, Firecrawl, and YouTube handling.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
