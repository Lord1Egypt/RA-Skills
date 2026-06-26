## Description: <br>
Compare two face images and return similarity score using iFlytek Face Recognition API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dzy-1026](https://clawhub.ai/user/Dzy-1026) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to compare two face images for identity verification, access control, duplicate-account checks, photo matching, security authentication, or attendance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected face images are sent to iFlytek for processing. <br>
Mitigation: Use the skill only with permission to process the subjects' biometric data and review iFlytek privacy and retention terms before security-sensitive use. <br>
Risk: Required API credentials could be exposed if mishandled. <br>
Mitigation: Store XF_FACE_APP_ID, XF_FACE_API_KEY, and XF_FACE_API_SECRET in protected environment configuration and avoid logging or sharing credential values. <br>


## Reference(s): <br>
- [iFlytek Face Recognition API documentation](https://www.xfyun.cn/doc/face/xf-silent-in-vivo-detection/API.html) <br>
- [ClawHub skill page](https://clawhub.ai/Dzy-1026/xfyun-face-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON response printed to stdout with status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires two local image paths and iFlytek API credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
