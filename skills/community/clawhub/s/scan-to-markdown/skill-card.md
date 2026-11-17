## Description:

OCR document extraction - extract text from scanned documents, photos, and images using OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract text from scanned PDFs, photographed pages, handwritten notes, and image files by invoking the MinerU Open API CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents are uploaded to MinerU's cloud API for OCR processing.

Mitigation: Avoid confidential, regulated, or private documents unless MinerU's terms and the processing model have been reviewed and accepted.

Risk: The skill relies on unpinned third-party CLI installation sources.

Mitigation: Use a pinned, reviewed installer version where possible and run OCR workflows in an isolated environment for sensitive use cases.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tanis90/skills/scan-to-markdown)
- [MinerU](https://mineru.net)
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and OCR result guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local files and URLs for PDF, PNG, JPG, WebP, BMP, and TIFF inputs up to 10MB or 20 pages, according to the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
