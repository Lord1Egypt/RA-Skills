## Description:

用 AI Hive Nano Banana Pro 将已授权成年模特图与已授权服装 SKU 图组合成可审核的虚拟试穿商品图，锁定人物身份与身体比例、服装版型与纹理、层叠遮挡和电商构图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Fashion sellers and brand teams use this skill to create authorized adult virtual try-on product images from model, garment SKU, and optional background references. It supports listing and lifestyle apparel previews while requiring authorization checks and treating outputs as visual previews rather than sizing or fit guarantees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive adult model, garment, and background images may be sent to AI Hive and storage endpoints returned by its API.

Mitigation: Use only consented and authorized source images, review AI Hive data-handling expectations before use, and avoid uploading unnecessary sensitive content.

Risk: Uploads and downloads use dynamically supplied HTTPS destinations without a documented host allowlist.

Mitigation: Run the skill in a controlled network environment and review returned upload or result URLs before allowing transfer of sensitive images.

Risk: Generated try-on images may be mistaken for real fit, sizing, or purchase guarantees.

Mitigation: Label outputs as visual previews, manually review identity, garment, and occlusion details, and avoid claims about actual fit or sizing.

Risk: API keys may be exposed through shell history or overly broad account access.

Mitigation: Prefer the AI_HIVE_API_KEY environment variable or the skill's auth storage flow, and use a dedicated key with limited quota.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/virtual-try-on-product-image-generation)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bash commands, Python CLI usage, and generated image file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key and authorized adult model, garment, and optional background image references.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
