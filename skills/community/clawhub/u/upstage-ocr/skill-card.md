## Description:

Extract plain text with word-level bounding box coordinates from images and scanned documents using the Upstage OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstage-deployment](https://clawhub.ai/user/upstage-deployment)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing agents use this skill to run OCR on images, scans, and supported document files when they need raw text plus word-level bounding boxes. It is not intended for layout-aware conversion or schema-driven field extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents submitted for OCR are sent to Upstage for processing.

Mitigation: Use the skill only for documents approved for third-party processing, and avoid highly confidential or regulated files unless that processing is acceptable.

Risk: Async OCR results are retained for a period of time and download URLs are refreshed through polling.

Mitigation: Use synchronous OCR when suitable, and apply the async workflow only when retention and polling behavior are acceptable for the document.

Risk: OCR results may be saved locally in a default temporary path.

Mitigation: Prefer a private, random, owner-only output path and share only the resolved path needed by the user.

## Reference(s):

- [Upstage OCR API documentation](https://console.upstage.ai/api/document-digitization/ocr)
- [ClawHub skill page](https://clawhub.ai/upstage-deployment/skills/upstage-ocr)

## Skill Output:

**Output Type(s):** [text, json, code, shell commands, guidance]

**Output Format:** [Markdown guidance with API examples and JSON OCR result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR results may include page text, word bounding boxes, confidence scores, usage counts, and a resolved output file path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
