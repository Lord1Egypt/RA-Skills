## Description:

批量将商品图片处理为适用于电商商品展示的纯白背景图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators can process one or many product photos into clean white-background images for marketplace listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product photos are uploaded to Qinghu AI for processing, and batch jobs may incur service charges.

Mitigation: Upload only images approved for that service; use estimate before large batches and review the quoted cost.

Risk: The qhkit command-line tool must be installed and configured with an API token.

Mitigation: Use a reviewed, pinned release, install without administrator privileges, keep the token private, and review upgrades.

Risk: Generative redraw may slightly change product details.

Mitigation: Review each result for text, logos, and product structure before delivery.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-white-background)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Publisher profile](https://clawhub.ai/user/autoagc)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands, Configuration instructions]

**Output Format:** [White-background JPG or PNG images with Markdown delivery notes and CLI setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch processing submits images one at a time. Results are generated redraws, not pixel-level edits or transparent alpha PNGs; review text, logos, and product structure.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
