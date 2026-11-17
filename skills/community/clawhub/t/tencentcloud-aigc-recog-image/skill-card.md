## Description:

TencentCloud Image AIGC Detection helps agents submit image URLs or supported local image files to Tencent Cloud ImageModeration for AI-generated image detection and receive a structured result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn233](https://clawhub.ai/user/shawn233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content review workflows use this skill to check whether an image appears AI-generated. The skill returns a pass, review, or block suggestion with score and label details from Tencent Cloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted image URLs or local image contents can be sent to Tencent Cloud for processing.

Mitigation: Use the skill only with images appropriate for Tencent Cloud processing and follow applicable data handling requirements.

Risk: Tencent Cloud SecretId, SecretKey, and BizType are required, and persistent plaintext shell-profile storage can expose credentials.

Mitigation: Prefer short-lived or least-privilege credentials where available, and avoid storing secrets in broadly loaded plaintext files such as shell startup profiles.

Risk: The release security verdict is suspicious because the skill can transmit local images and includes credential-handling guidance that needs review.

Mitigation: Review the skill before installing, use a dedicated virtual environment, and pin or review the Tencent SDK version.

## Reference(s):

- [ImageModeration API reference](references/image_moderation_api.md)
- [Tencent Cloud ImageModeration documentation](https://cloud.tencent.com/document/product/1125/53273)
- [Tencent Cloud SDK guide](https://cloud.tencent.com/document/product/1124/100983)
- [ClawHub skill page](https://clawhub.ai/shawn233/skills/tencentcloud-aigc-recog-image)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON detection result or JSON setup/error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include suggestion, label, score, optional detailed labels, and request ID.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
