## Description: <br>
Calls Tencent Cloud FaceID DetectAIFakeFaces to check face images or videos for AI face-swap, reshoot, abuse-pattern, watermark, and related anti-fraud attack signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzzhanglijie](https://clawhub.ai/user/hzzhanglijie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send authorized face image or video inputs to Tencent Cloud FaceID and receive anti-fraud risk results for face liveness and spoofing checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles and uploads highly sensitive face media to Tencent Cloud FaceID. <br>
Mitigation: Use it only when the user intentionally wants Tencent Cloud FaceID processing and has consent or another lawful basis for biometric data processing. <br>
Risk: The security summary says the skill lacks enough clear user-facing disclosure or consent controls before upload. <br>
Mitigation: Review before installing and prefer an updated version that requires explicit confirmation before sending face images or videos. <br>
Risk: Provider retention and privacy terms may affect whether a use case is acceptable. <br>
Mitigation: Check Tencent Cloud FaceID service terms and privacy requirements before processing face media. <br>


## Reference(s): <br>
- [Tencent Cloud DetectAIFakeFaces API documentation](https://cloud.tencent.com/document/product/1007/101561) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON response printed by a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns attack risk level, risk detail information, optional face detail information, and request ID when provided by the Tencent Cloud API.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
