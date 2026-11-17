## Description:

Convert Markdown reports to professionally formatted PDF documents using pdfkit, with support for Chinese fonts, A4 layout, automatic headers and footers, and page numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Markdown reports, trade journals, weekly reviews, and investment memos into formatted A4 PDF files for sharing or offline review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Node/pdfkit script that reads a Markdown file and writes a PDF file.

Mitigation: Review the input and output paths before execution, use a workspace-local output location, and avoid overwriting important files.

Risk: PDF generation depends on local pdfkit and font paths, including CJK-capable fonts for Chinese text.

Mitigation: Set PDFKIT_PATH when needed and verify that an appropriate TrueType or TrueType Collection font is available before generating production PDFs.

Risk: Generated PDFs may use default Chinese report title and page labels when no explicit title is supplied.

Mitigation: Provide an explicit report title when invoking the script if the default labels are not appropriate.

Risk: Complex tables or layout-heavy Markdown may not render with full CSS-like fidelity because styling is programmatic.

Mitigation: Inspect generated PDFs for table alignment, page breaks, headers, footers, page numbers, and content overflow before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaocaixia888/skills/zcx-pdf-report-generator)
- [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code, Guidance]

**Output Format:** [PDF file output with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local Markdown input file and writes a PDF output path; requires Node.js, pdfkit, and an available CJK-capable font for Chinese text.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
