## Description:

根据服装图和可选模特参考图，指导 qhkit 生成电商服装试穿展示图，并支持调整模特特征。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

服装卖家可用此技能将平铺或挂拍服装图转换为模特试穿展示图，也可把服装套用到指定模特参考图上，用于制作商品图片。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic software updates and returned upgrade commands need clear user control.

Mitigation: Review the package version and upgrade command before running; ask before elevated installation or shared configuration changes.

Risk: Selected images leave the device, and image generation consumes account credits.

Mitigation: Confirm the user has chosen the images and understands the upload and credit use before generation.

Risk: The external qhkit CLI implementation is unverified.

Mitigation: Prefer a reviewed package version in an isolated environment and inspect installation and upgrade commands.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-model-outfit-swap)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands]

**Output Format:** [Generated image files with concise command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated garment details may differ; review text, logos, and product structure.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
