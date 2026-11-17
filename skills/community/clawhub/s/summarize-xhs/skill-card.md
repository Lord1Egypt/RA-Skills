## Description:

Summarizes URLs, PDFs, images, audio files, and YouTube links with a configurable CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seeu1688](https://clawhub.ai/user/seeu1688)

### License/Terms of Use:

MIT

## Use Case:

Developers and content reviewers use this skill to summarize web pages, local documents, media files, and YouTube links from an agent workflow with configurable model and output options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party CLI install source.

Mitigation: Pin or otherwise verify the summarize binary and Homebrew tap before installation.

Risk: Submitted content may be sent to the active model provider or fallback extraction service.

Mitigation: Avoid confidential or regulated inputs unless the provider and fallback path are approved; use narrowly scoped API keys.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/seeu1688/skills/summarize-xhs)
- [ClawHub publisher profile](https://clawhub.ai/user/seeu1688)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI outputs plain text or JSON summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary length, token limit, extraction mode, fallback services, YouTube mode, and model can be configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
