## Description:

Extracts content from DOCX, XLSX, PDF, and image files and converts the extracted text and tables into Markdown, with OCR support for scanned PDFs and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinoslug](https://clawhub.ai/user/sinoslug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to read existing Word, Excel, PDF, and image documents and convert their contents into structured Markdown for review, analysis, or downstream agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local command and file-write authority despite being framed as read-only.

Mitigation: Review planned commands and generated files before execution, and run the skill in a restricted workspace when handling sensitive material.

Risk: OCR processing may expose confidential scans, screenshots, or document images to an external OCR service.

Mitigation: Avoid using the skill on confidential documents unless the OCR service's data handling is approved for that data.

Risk: Scanned PDF pages may be written as temporary images under /tmp.

Mitigation: Use private temporary paths and clean up rendered page images after extraction.

Risk: Dependency installation commands can affect the active Python environment.

Mitigation: Install dependencies in a dedicated virtual environment before running extraction workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional shell commands and OCR guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted document metadata, tables, OCR status, error guidance, and dependency installation commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
