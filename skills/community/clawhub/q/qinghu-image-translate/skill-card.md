## Description:

批量翻译商品图片中的文字内容，自动保持原有版式与设计风格，帮助跨境卖家完成多语言商品图本地化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

跨境电商卖家和商品内容团队可用此技能将商品主图与详情图中的文字转为目标语言，并批量生成本地化图片。完成后应核对译文、价格、规格、品牌标识和商品细节。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images are uploaded through the service workflow, and external CLI behavior and service retention practices are unverified.

Mitigation: Use only images authorized for Qinghu AI and avoid sending sensitive content. Prefer a reviewed CLI release.

Risk: Service credentials or image-generation credit costs may be mishandled.

Mitigation: Protect the service token, check credit costs before use, and keep qhkit configuration separate if it is already used for other work.

Risk: Generated lettering or product details may differ from the source image.

Mitigation: Visually check translations, prices, specifications, logos, and product structure before publishing the images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-image-translate)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands]

**Output Format:** [Generated image files with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch jobs process images individually; review generated text and important product details before use.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
