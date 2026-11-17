## Description:

免费复用用户已登录的浏览器，只读比较 2–5 个商品页面并生成含来源与读取日期的 Markdown 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

面向中文自媒体创作者和小店经营者，用于比较用户指定的 2–5 个商品页面可见信息，并整理成带来源、读取日期和选择建议的报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A signed-in browser profile can expose account-scoped page content during comparison.

Mitigation: Select the exact browser profile and product URLs to access, and review the separate browser and Bridge permissions before use.

Risk: Visible prices, stock, and after-sales terms may change or may not reflect final transaction conditions.

Mitigation: Record the read date and visible conditions, label unavailable details, and confirm current terms on the merchant page before purchase.

## Reference(s):

- [Easy WebBridge 项目与安装说明](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR 官方下载页](https://www.ebrower.com/down.html)
- [EasyBR v1.7.8 GitHub Release](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [中文 Markdown 商品对比报告，包含可见信息、来源链接、读取日期和选择建议。]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [比较 2–5 个用户指定页面；未显示或无法确认的字段会明确标注。]

## Skill Version(s):

1.0.3 (source: server-resolved release, manifest.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
