## Description:

Provides a Vipshop shopping assistant skill bundle for product search, product details, promotions, image-based search, and QR-code login workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vip](https://clawhub.ai/user/vip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill bundle to search Vipshop products, compare prices and discounts, inspect product details, browse promotions, find similar products from images, and manage QR-code login when required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login tokens may be exposed through displayed URLs or product links.

Mitigation: Do not display links containing PASSPORT_ACCESS_TOKEN or exchange-token credentials; redact or replace them with non-authenticated product detail links before showing results.

Risk: The skill can initiate login, image upload, or dependency installation too aggressively.

Mitigation: Require explicit user consent before starting QR-code login, uploading local images, or installing dependencies.

Risk: Unpinned dependencies may change behavior or introduce reviewed-surface drift.

Mitigation: Pin requests, qrcode, Pillow, and packaging to reviewed versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vip/skills/vip-skill)
- [唯品会扫码登录 API 接口文档](vipshop-user-login/references/api_reference.md)
- [唯品会扫码登录 - 其他技能集成指南](vipshop-user-login/references/integration_guide.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries with structured JSON from helper scripts and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product links, prices, discounts, images, promotion details, login status, and next-step guidance.]

## Skill Version(s):

1.0.6 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
