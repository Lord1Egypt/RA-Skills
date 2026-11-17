## Description:

一键生成服装的不同颜色版本，保持版型、材质及光影一致，无需重新拍摄即可完成 SKU 色卡图制作。当用户要求服装换色、出其他颜色版本、SKU 配色图、色卡图时必须触发。关键词：青虎AI、qhkit、服装换色、换色、改颜色、SKU图、色卡、配色版本、多色版本、免拍摄。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商卖家和商品运营人员可基于一张服装原图生成不同颜色的 SKU 配色图，并检查生成结果中的服装结构、文字与 logo。

### Deployment Geography for Use:

China (Qinghu domestic site)

## Known Risks and Mitigations:

Risk: Clothing images are uploaded to Qinghu, where retention terms and generation costs may matter.

Mitigation: Use images you are comfortable sending to Qinghu, and check its retention terms and generation costs.

Risk: The external qhkit executable package was not audited, and setup may change CLI configuration or shell settings.

Mitigation: Prefer a reviewed CLI version and inspect setup or upgrade commands before running them; protect the API key.

Risk: Generative recoloring may subtly alter garment details.

Mitigation: Review generated images for important text, logos, and product structure.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-clothing-recolor)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration guidance]

**Output Format:** [Generated clothing recolor images with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated garment details may vary slightly; review text, logos, and product structure.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
