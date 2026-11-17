## Description:

Provides Chinese Word document formatting standardization for titles, headings, body text, images, charts, and tables using Microsoft YaHei and consistent spacing, alignment, indentation, and page settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmtea1981](https://clawhub.ai/user/lmtea1981)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and document automation developers can use this skill to standardize Chinese .docx documents for enterprise documents, academic papers, reports, and similar materials. It is intended for workflows where consistent typography, paragraph spacing, indentation, image alignment, table formatting, and Chinese punctuation conventions are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The formatting script writes a new Word document and may not preserve every complex layout or special construct exactly as expected.

Mitigation: Run it on a copy of important documents, review the generated file, and manually adjust complex elements such as footnotes, endnotes, cross-references, image captions, or unusual styles.

Risk: The skill depends on python-docx for document processing.

Mitigation: Install dependencies in a controlled environment and consider pinning python-docx to a reviewed version before operational use.

Risk: The output relies on Microsoft YaHei for the intended Chinese typography.

Mitigation: Confirm the target system has Microsoft YaHei or an approved substitute installed before relying on the rendered appearance.

## Reference(s):

- [Word Chinese Formatting Standard](artifact/references/format_standard.md)
- [Word Chinese Formatting Usage Guide](artifact/references/usage_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/lmtea1981/skills/word-cn-format)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates .docx output files through the provided formatting script when executed by the user or agent.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
