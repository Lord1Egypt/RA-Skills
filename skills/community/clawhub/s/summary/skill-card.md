## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[anbring](https://clawhub.ai/user/anbring)

### License/Terms of Use:


## Use Case:

Developers and other agent users use this skill to summarize URLs, local files, PDFs, images, audio, and YouTube links through the summarize CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected content may be sent to external model or extraction providers.

Mitigation: Avoid using the skill on secrets, regulated data, or internal documents unless the selected providers are approved for that data.

Risk: The skill depends on a third-party CLI installed through Homebrew.

Mitigation: Review or pin the Homebrew package source before use in sensitive environments.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/anbring/skills/summary)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON output from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can request short through xxl summaries, custom character limits, max output tokens, extract-only mode, and provider-specific API keys.]

## Skill Version(s):

0.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
