## Description:

为小红书电商与品牌合作生成和编辑商品卡图片、笔记轮播、真实使用图、卖点证明及聚光广告素材，支持参考图保真及 AI Hive 生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, brand teams, and agents use this skill to plan and run AI Hive image generation or editing for Xiaohongshu product cards, note carousels, unboxing visuals, brand collaboration images, and ad creative hypotheses. The skill emphasizes accurate reference-product preservation, evidence-based claims, and review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI Hive API keys can be sent to a user-configurable API host when --base-url or AI_HIVE_BASE_URL is changed.

Mitigation: Use the default AI Hive endpoint unless the alternate host is fully trusted; install dependencies in an isolated environment with pinned versions when using a real API key.

Risk: Generated ecommerce images may imply unsupported product effects, reviews, discounts, platform labels, or conversion results.

Mitigation: Ground prompts in provided product evidence, keep claims and social proof out of generated images unless approved, and review against current Xiaohongshu community, ecommerce, and commercial-content rules before publication.

Risk: Reference images and product media are uploaded to the AI Hive workflow.

Mitigation: Use only media the operator is authorized to process and avoid sensitive personal, confidential, or unreleased brand assets unless the upload destination and retention terms are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/xiaohongshu-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files, Configuration]

**Output Format:** [Markdown guidance with bash command examples; generated image files or JSON task responses from AI Hive commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI_HIVE_API_KEY, optional AI_HIVE_BASE_URL or --base-url, optional reference images, batch count, routing mode, model parameters, output directory, and no-download mode.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
