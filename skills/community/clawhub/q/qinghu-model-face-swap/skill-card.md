## Description:

在保持服装、姿势不变的前提下替换商品图中的模特形象，支持不同国家、肤色及年龄，满足跨境电商本地化展示；视频里的人物替换同样支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

跨境电商运营者可用此技能将商品图片或视频中的模特替换为指定或描述的人物形象，以适配本地市场展示。替换真人肖像前需确认已获得使用授权，并检查生成结果中的商品细节。

### Deployment Geography for Use:

China (mainland; the skill documentation targets the domestic Qinghu service)

## Known Risks and Mitigations:

Risk: Selected media is uploaded to Qinghu, and generation may use account credits.

Mitigation: Use authorized media, review what will be uploaded, and use an appropriately scoped account or API key.

Risk: The instructions install or upgrade the latest qhkit release, while the external CLI implementation was not audited.

Mitigation: Use a reviewed CLI version and control updates; the artifact itself contains instructions rather than the CLI implementation.

Risk: Generative replacement can change small image details, including text, logos, or product structure.

Mitigation: Review generated media and verify key product details before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-model-face-swap)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Videos, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image or video media, with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image and video results may differ in small details; review text, logos, and product structure.]

## Skill Version(s):

0.1.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
