## Description:

This skill compares two face images with Tencent Cloud FaceID CompareFace and returns a similarity score and same-person judgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoqiangjava](https://clawhub.ai/user/xiaoqiangjava)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need to compare two face images, either from local image data or image URLs, and receive a Tencent Cloud similarity score with a threshold-based same-person judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected face images or image URLs are sent to Tencent Cloud for biometric comparison.

Mitigation: Use the skill only with appropriate consent and lawful authority, and avoid sensitive third-party faces unless privacy and compliance requirements are clear.

Risk: Tencent Cloud credentials are required to call the API.

Mitigation: Provide credentials with the minimum permissions needed for CompareFace and keep them out of prompts, logs, and shared artifacts.

## Reference(s):

- [Tencent Cloud CompareFace API documentation](https://cloud.tencent.com/document/product/867/44987)
- [ClawHub skill page](https://clawhub.ai/xiaoqiangjava/skills/tencentcloud-faceid-compareface)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON containing a similarity score, score description, same-person flag, model version, and request ID]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports image Base64 input, local image files converted to Base64, image URL input, optional quality control, and FaceModelVersion 2.0 or 3.0.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
