## Description:

为淘宝、天猫店铺生成和编辑商品主图、SKU 图、详情页卖点图、直通车与万相台广告图；支持商品参考图并通过 AI Hive 自动上传、生成、轮询和下载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, and developers use this skill to generate and edit Taobao and Tmall product main images, SKU images, detail-page benefit images, ad creatives, background replacements, and product-retouching outputs from supplied product references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom AI Hive base URL can redirect API requests and expose API keys or product reference images.

Mitigation: Use a dedicated API key, keep the default trusted endpoint unless a custom endpoint is fully trusted, and check environment variables and ~/.ai-hive/config.json before running.

Risk: Real commercial product images and paid API credentials are handled by the helper script.

Mitigation: Install and run the skill in an isolated environment, restrict access to the API key, and review outputs before publishing or reuse.

Risk: Generated ecommerce images may contain inaccurate product details, unsupported claims, or non-compliant ad text.

Mitigation: Compare generated assets against the supplied product facts, manually verify all text and claims, and check current Taobao or Tmall material rules before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/taobao-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and generated image files downloaded by the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated PNG files, task JSON, media IDs, and downloaded results under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
