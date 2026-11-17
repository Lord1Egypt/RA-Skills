## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tranhuilee](https://clawhub.ai/user/tranhuilee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to summarize web pages, local files, PDFs, images, audio files, and YouTube links through the summarize CLI. It supports provider-specific API keys, model selection, output length controls, JSON output, and optional extraction fallbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party Homebrew tap and summarize binary.

Mitigation: Install only after confirming that the tap, formula, and binary source are trusted for the intended environment.

Risk: Summarized content may be sent to configured AI providers or optional extraction services.

Mitigation: Do not process confidential local files, private URLs, or proprietary media unless provider terms and workplace policies allow that data transfer.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/tranhuilee/skills/skill-ts)
- [Publisher profile](https://clawhub.ai/user/tranhuilee)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with bash and JSON examples; the summarize CLI can produce text summaries or machine-readable JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output length, model, extraction-only mode, JSON mode, Firecrawl fallback, and YouTube fallback can be configured with CLI flags and API keys.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact/_meta.json, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
