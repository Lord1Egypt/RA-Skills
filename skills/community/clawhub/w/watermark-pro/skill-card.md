## Description:

Watermark Pro helps agents add text or logo watermarks to images, Word documents, PowerPoint files, and PDFs with diagonal, centered, or tiled layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate or adapt local Python watermarking helpers for image, DOCX, PPTX, and PDF files. It is suited to adding visible ownership, confidentiality, or branding marks to documents before sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Watermarking libraries read and rewrite local images, Office documents, and PDFs, which may include sensitive content.

Mitigation: Run the skill only on files the user has permission to process and use a private output directory for generated or rewritten documents.

Risk: Unpinned Python dependencies may change behavior or introduce compatibility issues over time.

Mitigation: Install dependencies in an isolated virtual environment and pin package versions before operational use.

Risk: PDF watermarking creates a temporary watermark image in the output directory during processing.

Mitigation: Use a controlled output directory and remove temporary files if a run is interrupted before cleanup completes.

## Reference(s):

- [Watermark Pro on ClawHub](https://clawhub.ai/tobewin/skills/watermark-pro)
- [tobewin publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code blocks and dependency installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Python packages including pillow, python-docx, python-pptx, and pymupdf; generated helpers read and rewrite local media or document files.]

## Skill Version(s):

1.0.4 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
