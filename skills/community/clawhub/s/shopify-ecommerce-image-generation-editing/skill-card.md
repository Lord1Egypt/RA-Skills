## Description:

Create and edit Shopify product photography, PDP image galleries, collection banners, DTC lifestyle images and campaign creatives for Shopify商品图、独立站PDP、Hero Image、产品套图、DTC品牌视觉、Meta Ads素材、邮件营销、换背景、多市场本地化和批量SKU with reference-guided generation through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, Shopify merchants, marketers, and developers use this skill to generate and edit consistent product, PDP gallery, collection, homepage, paid social, and email images from reference assets. The skill emphasizes preserving product and brand details while avoiding invented offers, reviews, claims, certifications, or legal text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials can be sent to a user- or environment-controlled AI Hive endpoint.

Mitigation: Use only a trusted AI Hive endpoint, avoid overriding `AI_HIVE_BASE_URL` or `--base-url` unless the destination is trusted, and use a limited API key.

Risk: Product images supplied as references are uploaded to the AI Hive service.

Mitigation: Confirm the images are approved for external processing before use and avoid uploading confidential or restricted assets.

Risk: Generated ecommerce imagery could introduce inaccurate product details, offers, claims, certifications, or legal text.

Mitigation: Review outputs against product references, brand requirements, Shopify theme constraints, and ad-channel policies before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/shopify-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and local configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can upload reference images, submit generation tasks, poll task status, and download generated image outputs through AI Hive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
