## Description: <br>
TencentCloud Image AIGC Detection helps agents submit an image URL or local image file to Tencent Cloud ImageModeration with IMAGE_AIGC detection and return the service's AI-generated image assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn233](https://clawhub.ai/user/shawn233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to check whether selected images appear AI-generated, including AI artwork review, image authenticity screening, synthetic media checks, and Deepfake detection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images or image URLs are processed by Tencent Cloud. <br>
Mitigation: Install and use the skill only when external Tencent Cloud processing is approved for the image data. <br>
Risk: Long-lived Tencent Cloud credentials may be exposed if stored in shared shell profiles. <br>
Mitigation: Use scoped or temporary Tencent Cloud credentials where possible and avoid storing long-lived secrets in shared environments. <br>
Risk: Private, biometric, regulated, or confidential images could be submitted to an external cloud service. <br>
Mitigation: Do not submit sensitive images unless the user or organization has explicit approval for that processing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shawn233/tencentcloud-aigc-recog-image) <br>
- [ImageModeration API reference](references/image_moderation_api.md) <br>
- [Tencent Cloud ImageModeration documentation](https://cloud.tencent.com/document/product/1125/53273) <br>
- [Tencent Cloud SDK guide](https://cloud.tencent.com/document/product/1124/100983) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses with concise user-facing guidance and setup commands when configuration is missing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results can include suggestion, label, score, sub-labels, detailed result arrays, error codes, and request IDs.] <br>

## Skill Version(s): <br>
1.0.8 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
