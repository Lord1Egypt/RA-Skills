## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to summarize URLs, local files, PDFs, images, audio, and YouTube links through the summarize CLI. It helps an agent provide setup guidance, shell commands, and configuration examples for the CLI and its supported provider keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send private documents, internal URLs, regulated data, secrets, or other user-provided content to the selected summarization provider or optional extraction services.

Mitigation: Use only approved provider keys and avoid submitting sensitive material unless the provider and data handling path are approved.

Risk: Installation depends on an unpinned third-party Homebrew tap and upstream CLI update process.

Mitigation: Install only if the publisher and Homebrew tap are trusted, and review the installed CLI version before use.

Risk: Provider and optional service API keys may be exposed if unrelated environment variables are shared with the CLI process.

Mitigation: Expose only the environment variables required for the selected provider or optional service.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/skill-0331-02)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can describe CLI flags, provider API key setup, optional service tokens, and machine-readable JSON output mode.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
