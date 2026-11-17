## Description:

TencentCloud MLIDPassport OCR calls Tencent Cloud OCR to extract passport identity fields, MRZ and visual-zone details, optional portrait crops, and international warning signals from passport images supplied by URL or Base64.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit authorized passport images to Tencent Cloud OCR and receive structured passport data for downstream review or workflow automation. It is suited to passport information extraction, MRZ parsing, optional portrait crop return, and international warning checks where Tencent Cloud OCR credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passport images, image URLs, extracted identity fields, and optional portrait crops contain highly sensitive personal data.

Mitigation: Process only documents the user is authorized to handle, minimize retention of submitted images and returned fields, and avoid enabling portrait crop return unless it is required.

Risk: The skill sends passport image data or image URLs to Tencent Cloud OCR for processing.

Mitigation: Install and use it only when Tencent Cloud processing is intended and acceptable for the relevant privacy, compliance, and data residency requirements.

Risk: Tencent Cloud credentials are required to call the OCR service.

Mitigation: Use restricted Tencent Cloud keys, store them in environment variables, rotate them regularly, and avoid sharing credentials in prompts, logs, or files.

Risk: The Tencent Cloud SDK dependency may change behavior if installed without version controls.

Mitigation: Pin and review the SDK dependency in managed environments before production deployment.

## Reference(s):

- [Tencent Cloud MLIDPassportOCR API Documentation](https://cloud.tencent.com/document/api/866/37657)
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/skills/tencentcloud-ocr-mlidpassport)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses and concise command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud OCR credentials and either an image URL or Base64 image input.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
