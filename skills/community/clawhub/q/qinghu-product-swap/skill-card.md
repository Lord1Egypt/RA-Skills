## Description:

一键替换图片中的商品主体，并尽量保留原场景、构图与光影，帮助复用电商素材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

外部电商运营者可用两张参考图将场景图中的旧商品替换为新品，并复用既有商品素材。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Reference images are uploaded to Qinghu, whose data handling and retention terms are not verified here.

Mitigation: Use only images authorized for upload and check Qinghu's retention terms before sending confidential material.

Risk: The separately downloaded CLI and its updates are not covered by the artifact scan.

Mitigation: Prefer a reviewed, pinned CLI version and review upgrade commands before running them.

Risk: Generated product details may differ from the reference image.

Mitigation: Review the result, especially text, logos, product structure, proportions, perspective, and reflections.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-product-swap)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image files, CLI JSON responses, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count is configurable from 1 to 10; generated product details may vary and should be reviewed.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
