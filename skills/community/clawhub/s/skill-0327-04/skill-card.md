## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to summarize URLs, local files, PDFs, images, audio, and YouTube links with the summarize CLI, including model and provider-key configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party Homebrew tap and the summarize CLI it installs.

Mitigation: Review and trust the tap and CLI before installation, and pin or audit the installed dependency according to local policy.

Risk: Files, URLs, and API keys passed to the CLI may be available to the CLI and configured AI or extraction providers.

Mitigation: Avoid sending sensitive documents or credentials unless the chosen provider and extraction path are approved for that data.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/skill-0327-04)
- [ClawHub publisher profile](https://clawhub.ai/user/yinwuzhe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The wrapped CLI can emit machine-readable JSON and supports length, token-limit, extraction, Firecrawl, and YouTube options.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact/_meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
