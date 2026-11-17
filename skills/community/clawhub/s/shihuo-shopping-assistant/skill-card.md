## Description:

根据用户的商品需求、商品图片或电商链接，提供商品推荐、规格与价格比较、优惠信息及购买入口。

This skill is ready for commercial/non-commercial use.

## Publisher:

[acmev](https://clawhub.ai/user/acmev)

### License/Terms of Use:

MIT-0

## Use Case:

消费者可通过关键词、图片或商品链接获取商品推荐、规格选择、渠道价格、历史走势和优惠信息，以辅助购物决策。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 访问凭据可能暴露，发送给购物服务的私密消息内容也可能被转发。

Mitigation: 仅连接经过验证的 HTTPS 服务，妥善保护凭据，并在转发前删去私密信息；不要在聊天中粘贴密钥。若已使用此版本的默认连接，请轮换凭据。

## Reference(s):

- [识货购物助手发布页](https://clawhub.ai/acmev/skills/shihuo-shopping-assistant)
- [识货开放平台](https://www.shihuo.cn/page/openPlatform)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [中文 Markdown 商品咨询回复，包含推荐、价格比较、优惠信息和购买入口]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [购物事实依据本轮服务结果；未提供的数据会省略。]

## Skill Version(s):

9.0.0 (source: server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
