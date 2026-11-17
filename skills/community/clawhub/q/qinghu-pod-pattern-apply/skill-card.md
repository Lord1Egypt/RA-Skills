## Description:

帮助电商卖家将印花图案合成到服装、帽子、杯子等商品图中，生成 mockup 效果图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商卖家和设计师可用此技能为 POD 商品制作印花展示图：提供图案及商品照片，或仅提供图案并描述商品，即可生成商品 mockup。

### Deployment Geography for Use:

China (connects to the domestic Qinghu AI service)

## Known Risks and Mitigations:

Risk: Uploaded images may contain confidential designs or personal photos.

Mitigation: Upload only images suitable for sharing with Qinghu AI and check its retention terms before sending sensitive material.

Risk: Generated mockups can alter print details.

Mitigation: Review key design elements, placement, and colors against the original artwork.

Risk: The external CLI and service-side data handling were not verified; use may consume credits and requires an API token.

Mitigation: Use a reviewed CLI release, control upgrades, protect the API token, and check the quoted or actual credit cost before relying on generation.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI](https://www.iqinghu.com)

## Skill Output:

**Output Type(s):** [Image files, Text guidance, Shell commands, Configuration instructions]

**Output Format:** [Generated product mockup images with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Print details may vary in generated images; check key design elements against the source.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
