## Description:

TencentCloud BizLicense OCR calls Tencent Cloud's BizLicenseOCR API to extract structured fields from business-license images supplied as a URL, Base64 string, or local image file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to recognize Chinese business-license images and return company details such as registration number, legal representative, registered capital, business scope, validity period, and image warning signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business-license images and extracted company details are sent to Tencent Cloud OCR for processing.

Mitigation: Install only in environments approved for sending these documents to Tencent Cloud, and confirm before uploading sensitive images.

Risk: The skill depends on Tencent Cloud API credentials and the Tencent Cloud Python SDK.

Mitigation: Use narrowly scoped Tencent Cloud credentials and prefer a pinned, reviewed SDK version.

## Reference(s):

- [Tencent Cloud BizLicenseOCR API documentation](https://cloud.tencent.com/document/api/866/36215)
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/skills/tencentcloud-ocr-bizlicense)

## Skill Output:

**Output Type(s):** [json, shell commands, guidance]

**Output Format:** [JSON object printed to stdout, with command-line usage guidance in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials and either an image URL or Base64/image-file input; responses may include warning metadata for copied or re-photographed licenses.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
