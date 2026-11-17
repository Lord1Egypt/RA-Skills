## Description:

Generate a polished PDF report or summary from findings, data, or tables gathered earlier in the conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seitzbg](https://clawhub.ai/user/seitzbg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other agent users use this skill to turn gathered conversation findings, data, or tables into a clean PDF deliverable using Typst.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local Typst source and PDF files and runs typst compile.

Mitigation: Install and use it only in workspaces where local file creation and Typst compilation are acceptable.

Risk: The published package references summary and report templates that are missing from the artifact.

Mitigation: Verify template availability before relying on the skill, or review any agent-created Typst layout before compiling the PDF.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seitzbg/skills/skeet-pdf-report)
- [Publisher profile](https://clawhub.ai/user/seitzbg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Typst source files, shell commands, and generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local .typ and .pdf files and reports the output path after compilation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
