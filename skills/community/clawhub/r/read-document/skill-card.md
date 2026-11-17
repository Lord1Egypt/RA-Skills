## Description:

Convert any document to markdown using Canonizr.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmillerbakewell](https://clawhub.ai/user/hmillerbakewell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert PDFs, images, office files, and other user-selected documents into markdown transcripts through Canonizr. It also supports health checks, service start and stop commands, and optional JSON metadata when document details are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chosen documents may contain sensitive text, images, or file contents that are processed through the local Canonizr pipeline.

Mitigation: Use the skill only with documents intended for conversion, and avoid sensitive files unless that local processing is acceptable.

Risk: The Canonizr service may remain running after document conversion work is complete.

Mitigation: Use the documented stop command when the service is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmillerbakewell/skills/read-document)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown transcript, optional JSON metadata, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Failed conversions return error messages; users may store markdown output separately to avoid re-processing.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
