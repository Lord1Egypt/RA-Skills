## Description:

Calls Tencent Cloud's high-accuracy static face liveness detection API to assess whether an input face image appears live or replayed, using either image Base64 data or an image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoqiangjava](https://clawhub.ai/user/xiaoqiangjava)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run Tencent Cloud face liveness checks for identity-verification workflows and to receive a structured score, live/not-live judgment, model version, and request ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive face images and sends them to Tencent Cloud for remote processing.

Mitigation: Use only images the operator is authorized to process and confirm applicable privacy, retention, and regional requirements before production use.

Risk: Full image URLs can be written to stderr logs.

Mitigation: Avoid sensitive or long-lived signed image URLs, restrict log access and retention, and prefer local image or Base64 input when URL exposure is a concern.

Risk: Tencent Cloud credentials are required to invoke the API.

Mitigation: Use tightly scoped credentials, store them in environment-specific secret management, and rotate them on a regular schedule.

## Reference(s):

- [Tencent Cloud DetectLiveFaceAccurate API documentation](https://cloud.tencent.com/document/product/867/48501)
- [ClawHub skill page](https://clawhub.ai/xiaoqiangjava/skills/tencentcloud-faceid-detectlivefaceaccurate)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON]

**Output Format:** [JSON result from a Python CLI, with stderr status and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials and accepts either image Base64 data, a local image path, or an image URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
