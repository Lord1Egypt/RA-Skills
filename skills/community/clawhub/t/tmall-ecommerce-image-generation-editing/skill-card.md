## Description:

为天猫旗舰店生成和编辑品牌主图、详情页视觉、店铺首页 Banner、新品首发与大促活动图片。Use this skill for 天猫电商图片、天猫旗舰店、品牌商品图、详情页KV、超级品牌日、618/双11活动底图、会员营销、SKU套图和品牌视觉统一；支持参考图保真及 AI Hive 自动生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, and design teams use this skill to generate and edit Tmall storefront product images, detail-page visuals, homepage banners, campaign base images, and member-marketing assets while preserving brand and product constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and selected media can be sent to a custom AI Hive-compatible endpoint if AI_HIVE_BASE_URL or --base-url is changed.

Mitigation: Use the default official API URL unless the alternate endpoint is fully trusted, and keep API keys scoped and protected.

Risk: The skill can process real brand assets and product images through a remote image-generation service.

Mitigation: Review data-sharing requirements before use and avoid submitting confidential or unapproved brand material.

Risk: Generated ecommerce visuals may contain inaccurate product details, brand usage, pricing, promotions, claims, or platform marks.

Mitigation: Perform human review against source product facts, brand guidelines, and current Tmall category, campaign, and advertising rules before publication.

Risk: Installing runtime dependencies without version constraints can introduce environment drift.

Mitigation: Install dependencies in a virtual environment and pin package versions for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/tmall-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Image files]

**Output Format:** [Markdown guidance with inline bash commands, plus downloaded generated image files from AI Hive tasks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports reference images, batch generation, model parameters, routing options, output directories, task polling, and submit-only mode.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
