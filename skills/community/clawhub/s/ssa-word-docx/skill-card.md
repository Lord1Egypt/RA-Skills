## Description:

Create, read, and edit Word documents (.docx) with support for templates, tables, and styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation users use this skill to create or modify DOCX files, especially quotation documents with templates, tables, and styling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes DOCX files to user-specified output paths, which can overwrite existing documents.

Mitigation: Verify output paths before running generated commands and write to a dedicated output directory when possible.

Risk: The DOCX workflow depends on python-docx and may vary with local package versions.

Mitigation: Install the dependency in a virtual environment and pin python-docx for repeatable releases.

Risk: The artifact is primarily a local quotation DOCX generator rather than a complete Word read/edit suite.

Mitigation: Review generated documents manually when using the skill for broader Word editing tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/ssa-word-docx)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Files]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and generated DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file processing; depends on python-docx for DOCX generation and editing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
