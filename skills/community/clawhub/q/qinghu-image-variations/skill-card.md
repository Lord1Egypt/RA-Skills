## Description:

基于一张商品图快速生成多种营销版本，支持不同背景、布局和设计风格，轻松量产广告素材。当用户要求一张图出多个版本、图片裂变、素材裂变、量产不同风格的商品图时必须触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

面向电商运营者和广告素材创作者，基于商品图生成不同背景、布局或设计风格的营销图片，用于素材轮换和 A/B 测试；生成后应核对文字、标志和商品结构等关键细节。

### Deployment Geography for Use:

China (mainland; the skill documents use with Qinghu's domestic service)

## Known Risks and Mitigations:

Risk: Product images are uploaded to Qinghu for generation.

Mitigation: Use only images you are comfortable uploading to the service.

Risk: Large generation batches can incur unexpected credit use.

Mitigation: Review the estimate before submitting a large batch.

Risk: Automatic CLI updates can change behavior, and downloaded CLI code and future releases were outside the security assessment.

Mitigation: Use a reviewed, fixed CLI version and control upgrades.

Risk: The service token may persist in local configuration.

Mitigation: Protect the token and limit access to the local configuration that stores it.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-image-variations)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image variations with concise command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports batches of 1, 2, 4, 6, 8, or 10 images; generated product details may vary and should be reviewed.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
