## Description:

唯品会（vip.com）图片搜索商品技能，当用户想通过图片搜索相似商品时触发，并返回商品名称、价格、品牌、图片、链接等结构化信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vip](https://clawhub.ai/user/vip)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search VIPShop for similar products from a local image and receive structured product results. It supports image upload, category recognition, paginated product search, and Markdown presentation of returned product data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated product links may contain encoded session-token data from a saved VIPShop login.

Mitigation: Avoid sharing generated links or transcripts, and require review before installation until token-bearing URLs are removed or redacted.

Risk: The skill reads saved VIPShop login state and uploads user-provided images to VIPShop services.

Mitigation: Use only with explicit user consent, a VIPShop account intended for this workflow, and non-sensitive images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vip/skills/vipshop-img-product)
- [Publisher profile](https://clawhub.ai/user/vip)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown table for users, with JSON emitted by the bundled Python scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are paginated and return up to 10 products per page.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
