## Description:

Helps agents process PDF files, including text and table extraction, merging, splitting, rotation, watermarking, PDF creation, form handling, encryption, image extraction, and OCR-backed PDF-to-Markdown conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihaha123123123123](https://clawhub.ai/user/xixihaha123123123123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manipulate PDFs, extract text and tables, create new PDFs, and fall back to OCR when normal text extraction fails. It is especially relevant for scanned, photographed, image-heavy, or Chinese-language PDFs that need Markdown output with local image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OCR/PDF-to-Markdown path uploads complete PDFs to WPS using ambient WPS session credentials.

Mitigation: Use the OCR path only for PDFs approved for remote WPS processing, and avoid confidential, regulated, financial, legal, or proprietary documents unless that remote processing is explicitly acceptable.

Risk: The WPS_API_BASE setting and image download behavior affect where network requests go and what files are written locally.

Mitigation: Review and constrain WPS_API_BASE and image download behavior before use, and run conversions in an isolated output directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xixihaha123123123123/skills/wps-pdf)
- [WPS API Base](https://api.wps.cn)
- [WPS KDocs Web Origin](https://365.kdocs.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples; the OCR helper writes content.md and localized image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The OCR path may create Markdown and image files and sends complete PDFs to WPS using local WPS session credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
