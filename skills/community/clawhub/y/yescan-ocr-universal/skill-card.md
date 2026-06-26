## Description: <br>
This skill routes a single image URL, local image file, or Base64 image to Quark Scan King's OCR service for text extraction and structured recognition across documents, identity cards, invoices, forms, formulas, medical reports, business licenses, product images, and general images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozhihuidage](https://clawhub.ai/user/mozhihuidage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to extract text or structured fields from one static image using Quark Scan King's OCR scenes. It is suited to OCR workflows for handwritten notes, tables, IDs, tickets, invoices, formulas, questions, medical reports, business licenses, product images, and general text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted images and the API key are sent to Quark's OCR service. <br>
Mitigation: Use the skill only when third-party processing is acceptable, and prefer a dedicated or revocable SCAN_WEBSERVICE_KEY. <br>
Risk: OCR inputs may contain sensitive identity, medical, financial, or business documents. <br>
Mitigation: Avoid submitting highly sensitive documents unless the user or organization has approved Quark's handling of that data. <br>
Risk: The skill supports only one static image per invocation and local files are limited to 5 MB. <br>
Mitigation: Pre-process unsupported files by extracting a single image, converting to a supported image type, or compressing/cropping before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mozhihuidage/yescan-ocr-universal) <br>
- [Publisher profile](https://clawhub.ai/user/mozhihuidage) <br>
- [Quark Scan King business OCR platform](https://scan.quark.cn/business) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses from the OCR service, with setup and execution guidance in Markdown and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SCAN_WEBSERVICE_KEY; each invocation accepts exactly one image input as a URL, local file path, or Base64 string.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
