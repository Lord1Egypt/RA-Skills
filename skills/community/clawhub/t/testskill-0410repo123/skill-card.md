## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to ask an agent for summarize CLI commands and configuration for summarizing URLs, local files, PDFs, images, audio, and YouTube links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided files or links may be sent to the selected model provider, and to Firecrawl or Apify when those fallback services and tokens are enabled.

Mitigation: Avoid private documents, confidential URLs, and regulated data unless the relevant provider data policies are acceptable for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/testskill-0410repo123)
- [Summarize homepage](https://summarize.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that rely on local CLI installation, model-provider API keys, and optional extraction-provider tokens.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
