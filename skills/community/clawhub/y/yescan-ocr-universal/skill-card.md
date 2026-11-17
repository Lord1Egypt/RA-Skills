## Description:

Provides OCR for images, screenshots, and scanned documents through Quark Scan King, including printed text, handwriting, tables, formulas, IDs, invoices, tickets, medical reports, business licenses, and other supported document types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yescan-ai](https://clawhub.ai/user/yescan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit a single image, local image file, or base64 image to Quark Scan King's OCR service and receive extracted text or structured OCR data for supported document scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted images, including sensitive documents, are sent to Quark's remote OCR service using the configured API key.

Mitigation: Use only with documents approved for third-party OCR processing, and avoid submitting sensitive images unless that data flow is acceptable.

Risk: Crafted image inputs could be run unsafely as shell commands under the current command template.

Mitigation: Invoke Python with a non-shell argument array before routine use, and avoid untrusted image URLs, paths, or base64 strings until the run instructions are changed.

Risk: OCR POST requests allow redirects, which can broaden where submitted content and credentials are sent.

Mitigation: Disable or constrain redirects for OCR POST requests before routine use.

## Reference(s):

- [Quark Scan King Business Platform](https://scan.quark.cn/business)
- [ClawHub Skill Page](https://clawhub.ai/yescan-ai/skills/yescan-ocr-universal)

## Skill Output:

**Output Type(s):** [text, JSON, structured data]

**Output Format:** [JSON OCR response with code, message, and data fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAN_WEBSERVICE_KEY and sends submitted image content to Quark's remote OCR service.]

## Skill Version(s):

1.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
