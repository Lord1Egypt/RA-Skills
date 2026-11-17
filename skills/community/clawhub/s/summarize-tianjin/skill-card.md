## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianjin-ren](https://clawhub.ai/user/tianjin-ren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can use this skill to summarize web pages, local documents, images, audio, and YouTube links through the summarize CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party CLI that may change behavior after installation.

Mitigation: Review the upstream summarize CLI and Homebrew tap before installation and pin or audit the installed version where operational controls require it.

Risk: Local files, private URLs, and extracted content may be processed by the selected model provider or optional fallback services.

Mitigation: Avoid confidential, regulated, or private inputs unless the selected provider and any enabled fallback service are approved for that data.

Risk: Multiple API keys may be available in the environment, increasing exposure if unnecessary credentials are configured.

Mitigation: Set only the API key required for the chosen provider and omit optional service tokens unless those fallbacks are needed.

## Reference(s):

- [Summarize CLI homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/tianjin-ren/skills/summarize-tianjin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and configuration examples; the CLI can emit plain text or JSON summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable model provider, summary length, maximum output tokens, extraction-only mode, and optional fallback services.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
