## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbmchina](https://clawhub.ai/user/xbmchina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to summarize web pages, local documents, images, audio, and YouTube links through the summarize CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files, web content, and media may be sent to selected model providers or optional extraction services.

Mitigation: Avoid using the skill on secrets, confidential documents, regulated data, or private pages unless those providers and services are approved for that content.

Risk: The skill depends on installing and running a third-party CLI from a Homebrew tap.

Mitigation: Install only after confirming that the summarize CLI and the steipete/tap Homebrew source are trusted in the target environment.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/xbmchina/skills/summarize-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON summaries with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Length can be adjusted with CLI flags such as --length and --max-output-tokens.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
