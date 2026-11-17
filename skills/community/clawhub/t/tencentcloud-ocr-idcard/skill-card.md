## Description:

Calls Tencent Cloud IDCardOCR to extract fields from images of mainland China resident ID cards, with support for Base64 or URL image input, card-side detection, photo cropping, and warning signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit authorized ID-card images to Tencent Cloud OCR and receive structured identity fields and warning details. It is intended for workflows that need machine-readable OCR output for the front or back side of a mainland China resident ID card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes highly sensitive ID-card images and OCR results through Tencent Cloud.

Mitigation: Use it only with images the operator is authorized to process, and confirm the data-handling requirements for Tencent Cloud before submitting images.

Risk: Tencent Cloud credentials are required for API access.

Mitigation: Store TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY in a protected secret store and avoid writing them into prompts, scripts, logs, or shell history.

Risk: A readable local path passed as Base64 input may cause a non-image file to be uploaded.

Mitigation: Pass only intended image files, avoid arbitrary local paths, and run the skill in a restricted environment until file-type validation is added.

## Reference(s):

- [Tencent Cloud IDCardOCR API Documentation](https://cloud.tencent.com/document/api/866/33524)
- [ClawHub Skill Page](https://clawhub.ai/zt1314p-design/skills/tencentcloud-ocr-idcard)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration]

**Output Format:** [JSON emitted by a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes recognized ID-card fields, request ID, AdvancedInfo, and parsed warning codes when returned by Tencent Cloud.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
