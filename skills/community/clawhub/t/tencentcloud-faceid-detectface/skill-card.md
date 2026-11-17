## Description:

Calls Tencent Cloud FaceID DetectFace to detect faces in images and return structured face location, optional attribute, and optional quality results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoqiangjava](https://clawhub.ai/user/xiaoqiangjava)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run Tencent Cloud face detection against a local image, Base64 image, or image URL and receive JSON results for face counts, bounding boxes, attributes, and quality signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload any readable local file supplied as an image path to Tencent Cloud.

Mitigation: Use only intended image files, avoid arbitrary local paths, and run the skill in a restricted environment.

Risk: Face images and derived biometric attributes may involve sensitive personal data.

Mitigation: Use images with appropriate consent and review privacy requirements before enabling attribute or quality detection.

Risk: Tencent Cloud credentials are required for API calls.

Mitigation: Use narrowly scoped credentials stored in environment variables and rotate or revoke them according to local policy.

Risk: The artifact depends on an unpinned Tencent Cloud SDK installation.

Mitigation: Pin and review dependencies before broad deployment.

## Reference(s):

- [Tencent Cloud DetectFace API documentation](https://cloud.tencent.com/document/product/867/44989)
- [ClawHub skill page](https://clawhub.ai/xiaoqiangjava/skills/tencentcloud-faceid-detectface)
- [ClawHub publisher profile](https://clawhub.ai/user/xiaoqiangjava)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Shell commands, Guidance]

**Output Format:** [JSON returned by a command-line Python script, with setup and usage guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials in environment variables and may submit image data to Tencent Cloud.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
