## Description:

唯品会（vip.com）电商服务技能包，帮助代理登录唯品会、搜索商品、查看商品详情、浏览促销活动，并通过图片搜索相似商品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vip](https://clawhub.ai/user/vip)

### License/Terms of Use:

MIT-0

## Use Case:

External shopping users and shopping-assistant agents use this skill to complete Vipshop shopping workflows, including QR-code login, keyword search, image-based product search, product-detail lookup, and promotion discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product links produced while logged in may contain Vipshop login-session material visible in chat, logs, screenshots, or copied links.

Mitigation: Avoid sharing logged-in transcripts, logs, screenshots, or copied product links; prefer a fixed release that returns ordinary product URLs or short-lived server-side redirects.

Risk: The skill stores and reuses a local Vipshop login session for later API calls.

Mitigation: Use it only on trusted devices, keep the token file private, and clear the local Vipshop login session when the shopping workflow is complete.

Risk: Image-search workflows upload selected local images to Vipshop services.

Mitigation: Upload only images intended for Vipshop search and avoid images containing sensitive personal or confidential content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vip/skills/vip-skills)
- [Vipshop QR Login API Reference](artifact/vipshop-user-login/references/api_reference.md)
- [Vipshop Login Integration Guide](artifact/vipshop-user-login/references/integration_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries with structured JSON from helper scripts and Vipshop product links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include QR-code login status, product tables, prices, promotion details, image-search results, and links derived from the user's active Vipshop session.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
