## Description:

Compare two face images and return similarity score using iFlytek Face Recognition API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzy-1026](https://clawhub.ai/user/dzy-1026)

### License/Terms of Use:


## Use Case:

Developers and external operators use this skill to compare two face images for identity verification, authentication, duplicate account detection, and security workflows through the iFLYTEK Face Recognition API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected face images to iFLYTEK for remote biometric processing.

Mitigation: Use it only with appropriate consent and approval for biometric processing, and avoid running it on images that should not leave the local environment.

Risk: The security summary identifies avoidable credential and logging exposure risks.

Mitigation: Use dedicated, restricted iFLYTEK credentials and avoid logging or sharing failures until signed URL and exception redaction are improved.

## Reference(s):

- [iFLYTEK Face Recognition API documentation](https://www.xfyun.cn/doc/face/xf-silent-in-vivo-detection/API.html)
- [ClawHub skill page](https://clawhub.ai/dzy-1026/skills/xfyun-face-compare)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON with plain-text status and error messages printed to standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes similarity score, comparison result, confidence, face detection status, and raw API response when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
