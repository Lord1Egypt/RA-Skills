## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent summarize URLs, local files, PDFs, images, audio, and YouTube links through the third-party summarize CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Content submitted for summarization may be sent to configured model or extraction providers.

Mitigation: Do not summarize sensitive, regulated, or confidential files or URLs unless those disclosures are approved.

Risk: The skill depends on a third-party summarize CLI installed through a Homebrew tap.

Mitigation: Review the Homebrew tap and CLI source before installing in a high-trust environment.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/bingze00000/skills/summarize-jarvis)
- [Publisher profile](https://clawhub.ai/user/bingze00000)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON output when the summarize CLI is invoked with --json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
