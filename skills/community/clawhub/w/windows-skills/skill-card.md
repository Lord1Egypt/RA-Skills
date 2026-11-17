## Description:

Windows desktop automation skills - screenshot capture, OCR text extraction, and image-based UI element location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[civen-cn](https://clawhub.ai/user/civen-cn)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to capture Windows screen or window images, extract OCR text from screenshots, and locate UI elements by image matching for desktop automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshot capture and OCR can expose secrets, private documents, or other sensitive on-screen data.

Mitigation: Limit captures to the smallest needed region or window, avoid sensitive screens, store screenshots only in intended locations, and delete captures after use.

Risk: Desktop automation dependencies and OCR tooling expand the local execution surface.

Mitigation: Install dependencies in an isolated environment and use reviewed or pinned package versions.

## Reference(s):

- [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce screenshot image files, OCR text, text bounding boxes, and image-match coordinates when its helper scripts are used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
