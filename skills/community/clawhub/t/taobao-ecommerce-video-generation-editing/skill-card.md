## Description:

为淘宝、天猫商品页、店铺首页、上新与推广生成和编辑商品视频，支持文生、图生、参考生成、现有视频重制与 AI Hive 自动下载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, and developers use this skill to plan, generate, edit, poll, and download product videos for Taobao, Tmall, storefront, launch, live-preview, SKU, and paid promotion workflows. It emphasizes accurate product presentation, verified selling points, and platform-rule checks before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom API base URL can receive the user's AI Hive API key.

Mitigation: Use a dedicated API key and avoid AI_HIVE_BASE_URL or --base-url unless the endpoint is fully trusted.

Risk: Unpinned dependencies and local configuration can affect runtime behavior.

Mitigation: Install dependencies in a virtual environment with pinned versions and keep the API key in a protected local configuration file or environment variable.

Risk: Generated ecommerce videos may include unverified claims, pricing, certifications, discounts, or platform marks.

Mitigation: Review product facts and current Taobao or Tmall publishing rules before using generated media in listings or ads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/taobao-ecommerce-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key; can upload local media, poll generation tasks, and optionally download generated video outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
