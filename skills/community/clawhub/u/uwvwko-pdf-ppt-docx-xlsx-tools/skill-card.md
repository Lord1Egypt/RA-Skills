## Description:

Document conversion and extraction toolkit for PDF, PPTX, DOCX, and XLSX files, including image rendering, text and table extraction, merge, split, and watermark operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uwvwko-zzz](https://clawhub.ai/user/uwvwko-zzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-operations users use this skill to generate local commands and scripts for converting, extracting, merging, splitting, and watermarking PDF and Office documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require users to install Python packages or LibreOffice before conversions work.

Mitigation: Review package and system install commands before execution and install only the dependencies needed for the chosen conversion.

Risk: Generated HTML from DOCX content can preserve untrusted document text without sanitization.

Mitigation: Do not open, publish, or host generated HTML from untrusted documents until it has been reviewed and sanitized.

Risk: Document parsers and converters process user-selected local files and write to user-selected output paths.

Mitigation: Run conversions only on intended documents in controlled directories and inspect generated outputs before sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/uwvwko-zzz/skills/uwvwko-pdf-ppt-docx-xlsx-tools)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local document outputs such as PDF, DOCX, PPTX, XLSX, CSV, JSON, TXT, HTML, and image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
