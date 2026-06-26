## Description: <br>
Calls Tencent Cloud's DetectLiveFaceAccurate API to perform high-accuracy static face liveness checks on face images supplied as local files, Base64 strings, or image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoqiangjava](https://clawhub.ai/user/xiaoqiangjava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external teams use this skill to run Tencent Cloud static face liveness checks for anti-replay workflows, including checks against screen replay, printed-photo, and mask-style attacks. It returns a score and threshold-based live/spoofed judgment for the submitted image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face images or image URLs are submitted to Tencent Cloud for processing. <br>
Mitigation: Use the skill only when users have authorization or consent for the faces submitted and third-party cloud processing of biometric data is acceptable. <br>
Risk: Tencent Cloud API credentials are required to call the service. <br>
Mitigation: Store TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY securely, and avoid exposing credentials in logs, screenshots, or shared command output. <br>


## Reference(s): <br>
- [Tencent Cloud DetectLiveFaceAccurate documentation](https://cloud.tencent.com/document/product/867/48501) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON response with liveness score, score description, boolean live judgment, model version, and request ID.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials and accepts a local image file, Base64 image string, or image URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
