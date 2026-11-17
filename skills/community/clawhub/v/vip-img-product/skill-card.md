## Description:

唯品会（vip.com）图片搜索商品技能。当用户想通过图片搜索相似商品时触发，包括但不限于：以图搜图、拍照搜商品、图片搜索、找同款等。返回商品名称、价格、品牌、图片、链接等结构化信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vip](https://clawhub.ai/user/vip)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers or shopping assistants use this skill to search Vipshop for visually similar products from a local image and present structured product results. It is intended for image-to-product lookup workflows that need product names, prices, brands, images, links, and pagination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated product links may expose a user's Vipshop login token.

Mitigation: Do not share generated product links until the token-in-link behavior is removed or proven safe.

Risk: User-provided images are uploaded to Vipshop during search.

Mitigation: Use only images the user is willing to upload to Vipshop, and add explicit confirmation for account-token use and image upload.

Risk: Product-link generation relies on a hard-coded signing secret.

Mitigation: The publisher should remove the hard-coded signing secret before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vip/skills/vip-img-product)
- [Vipshop image upload endpoint](https://mapi-file-tx.vip.com/xupload/picture/new_upload_inner_applet.jsps)
- [Vipshop image category endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/search/img/category/v1)
- [Vipshop image product list endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/image/product/list/v1)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [JSON from the script, usually rendered by the agent as Markdown product tables and follow-up guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local image path or cached pagination values and an authenticated Vipshop login token.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
