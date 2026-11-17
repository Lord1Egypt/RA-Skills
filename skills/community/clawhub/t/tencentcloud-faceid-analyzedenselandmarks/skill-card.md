## Description:

Calls Tencent Cloud's AnalyzeDenseLandmarks API to detect faces and return bounding boxes plus dense facial landmark coordinates for eyes, eyebrows, mouth, nose, pupils, centerline, chin, eye bags, and forehead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoqiangjava](https://clawhub.ai/user/xiaoqiangjava)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to call Tencent Cloud face recognition for dense facial landmark extraction from a local image, Base64 image string, or image URL. It supports face-shape analysis, face alignment workflows, and coordinate extraction for up to five faces per image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face images, image URLs, and returned facial landmark data can be sensitive personal data.

Mitigation: Use the skill only when users are comfortable sending the selected image or URL to Tencent Cloud for processing, and handle outputs according to the applicable privacy requirements.

Risk: Tencent Cloud API keys are required and could be exposed through logs, repositories, or overly broad credentials.

Mitigation: Use least-privilege Tencent Cloud credentials, keep TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY out of logs and repositories, and rotate credentials when exposure is suspected.

Risk: Unpinned dependency installation can introduce supply-chain drift in production environments.

Mitigation: Prefer a pinned or locked installation of tencentcloud-sdk-python for production deployments.

## Reference(s):

- [Tencent Cloud AnalyzeDenseLandmarks documentation](https://cloud.tencent.com/document/product/867/47397)
- [ClawHub skill page](https://clawhub.ai/xiaoqiangjava/skills/tencentcloud-faceid-analyzedenselandmarks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance and shell commands; script execution returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud API credentials and returns face metadata, landmark coordinates, request IDs, and per-region API results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
