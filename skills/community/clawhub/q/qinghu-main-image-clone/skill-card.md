## Description:

参考爆款商品图片，智能分析其设计风格并用你的商品生成相似视觉效果，快速打造高点击率主图。当用户要求照着某张爆款图做主图、对标竞品主图、复刻图片风格时必须触发。关键词：青虎AI、qhkit、主图复刻、爆款复刻、对标主图、竞品图风格、风格迁移、照着做、相似风格主图、高点击率主图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and marketing teams use this skill to create product hero images that borrow the composition and visual style of a reference image while depicting their own product.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external qhkit CLI may change when installed or updated.

Mitigation: Review the CLI version before installation or updates and pin a reviewed release where practical.

Risk: Selected images are uploaded to Qinghu AI and image generation uses account credits.

Mitigation: Use images approved for upload and check the account-credit implications before generating.

Risk: The service token grants account access.

Mitigation: Keep the token private and avoid exposing it in shared commands or logs.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-main-image-clone)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands]

**Output Format:** [Generated product image(s) with concise Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image details may vary; users should check product structure, text, and logos.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
