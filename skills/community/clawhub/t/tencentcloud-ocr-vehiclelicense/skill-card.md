## Description:

Calls Tencent Cloud VehicleLicenseOCR to extract vehicle-license front, back, double-sided, electronic, and tractor-license fields from image URL, Base64, or local file inputs, including recognition warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to submit vehicle-license images to Tencent Cloud OCR and receive structured vehicle-license fields, warning codes, and request identifiers. It is suited for workflows that need front-side, back-side, double-sided, electronic, or tractor vehicle-license recognition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The file-path upload path can send any readable local file to Tencent Cloud if misused.

Mitigation: Run the skill in a restricted environment, pass only intended vehicle-license image files or trusted image URLs, and avoid broad filesystem access during agent-driven invocations.

Risk: Tencent Cloud credentials are required for execution.

Mitigation: Set Tencent Cloud credentials only for this skill's run and avoid sharing them with unrelated tools or broader agent sessions.

Risk: Vehicle-license images and extracted fields can contain personal or sensitive information.

Mitigation: Use explicit privacy notice or consent, validate the intended image content before submission, and handle OCR results according to the applicable data policy.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin the Tencent Cloud SDK dependency in deployment environments and review dependency updates before use.

## Reference(s):

- [Tencent Cloud VehicleLicenseOCR API Documentation](https://cloud.tencent.com/document/api/866/36209)
- [ClawHub Skill Page](https://clawhub.ai/zt1314p-design/skills/tencentcloud-ocr-vehiclelicense)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON recognition result with optional command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud OCR credentials and sends image URL or Base64/file-derived image content to Tencent Cloud.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
