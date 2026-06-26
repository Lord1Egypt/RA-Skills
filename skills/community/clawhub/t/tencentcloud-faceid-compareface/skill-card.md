## Description: <br>
Calls Tencent Cloud FaceID CompareFace to compare two face images, return a similarity score, and indicate whether they appear to be the same person. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoqiangjava](https://clawhub.ai/user/xiaoqiangjava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to run a Tencent Cloud 1:1 face comparison workflow for two authorized images or image URLs and return a similarity result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes biometric face images and may send local image data or supplied image URLs to Tencent Cloud for comparison. <br>
Mitigation: Use only images you have permission to compare, use least-privileged Tencent Cloud credentials, and avoid remote URLs unless provider processing is intended. <br>
Risk: Broad triggering and limited consent or privacy disclosure can lead to ambiguous or unintended face comparison requests. <br>
Mitigation: Require explicit user intent and consent before running comparisons, and review image inputs before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoqiangjava/tencentcloud-faceid-compareface) <br>
- [Tencent Cloud CompareFace API documentation](https://cloud.tencent.com/document/product/867/44987) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Score, ScoreDesc, IsSamePerson, FaceModelVersion, and RequestId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
