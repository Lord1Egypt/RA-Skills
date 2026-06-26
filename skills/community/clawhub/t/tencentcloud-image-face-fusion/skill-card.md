## Description: <br>
Uses Tencent Cloud's FuseFaceUltra API to fuse a user face image with a template image and return a generated result image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neck-cn](https://clawhub.ai/user/Neck-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to run Tencent Cloud image face fusion on supplied face and template images, with optional model selection and AI-label settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected face and template images are sent to Tencent Cloud for processing. <br>
Mitigation: Process only images the user has permission to use and disclose the external Tencent Cloud processing path before deployment. <br>
Risk: Tencent Cloud API credentials and account quota are required. <br>
Mitigation: Use least-privileged Tencent API keys, avoid hardcoding secrets, and prefer controlled secret storage over long-lived shell startup exports. <br>
Risk: The script can install the Tencent Cloud SDK at runtime if it is missing. <br>
Mitigation: Preinstall or pin the SDK in controlled environments before using the skill. <br>
Risk: The skill can disable the AI-generated content label with a runtime option. <br>
Mitigation: Keep AI-generated labeling enabled unless there is a legitimate reviewed reason to disable it. <br>


## Reference(s): <br>
- [TencentCloud Image Face Fusion Skill Page](https://clawhub.ai/Neck-cn/tencentcloud-image-face-fusion) <br>
- [Tencent Cloud FuseFaceUltra API](https://cloud.tencent.com/document/product/670/106891) <br>
- [Local FuseFaceUltra API Reference](references/FuseFaceUltraApi.md) <br>
- [Tencent Cloud Face Fusion Console](https://console.cloud.tencent.com/facefusion) <br>
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [JSON result containing a fused image URL or a structured error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials and sends selected input images to Tencent Cloud.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
