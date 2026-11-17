## Description:

Convert learning materials such as Word documents, PDFs, and images into QuickClass quiz JSON for single-choice, multiple-choice, and true/false questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makerguan](https://clawhub.ai/user/makerguan)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, teaching-support staff, and agent operators use this skill to convert exam papers, worksheets, and other learning materials into QuickClass-compatible classroom assignment JSON. It also guides handling image-based questions by producing supplemental image documentation when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted image mapping file may cause the image-document helper to read and embed local image files outside the intended folder.

Mitigation: Process only trusted mapping JSON files, review generated DOCX image documents before sharing, and avoid using the image-document helper with untrusted mappings until path confinement is added.

## Reference(s):

- [QuickClass JSON Schema](references/quickclass_schema.md)
- [ClawHub Skill Page](https://clawhub.ai/makerguan/skills/quickclass-quiz-converter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON files and optional DOCX image documents, with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports QuickClass question records for SINGLE_CHOICE, MULTIPLE_CHOICE, and TRUE_FALSE items.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
