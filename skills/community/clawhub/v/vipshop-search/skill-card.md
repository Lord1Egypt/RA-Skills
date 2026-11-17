## Description:

在唯品会搜索商品、比价和查找折扣，并通过本地 Python 脚本返回商品名称、品牌、价格、折扣、原价、图片和商品链接等结构化结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[viphgta](https://clawhub.ai/user/viphgta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to search Vipshop products, compare prices and discounts, browse paged results, filter by price, and request detail lookup for a selected product.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Vipshop login tokens and makes authenticated Vipshop requests.

Mitigation: Install and run it only in environments where the user accepts authenticated account access, and review token handling before use.

Risk: Product links may contain recoverable account credentials through exchange-token URL behavior.

Mitigation: Avoid sharing generated product links outside the active user session and fix token-in-URL behavior before normal use.

Risk: The skill can automatically start or install a separate Vipshop login workflow.

Mitigation: Require user approval for login setup and installation steps in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viphgta/skills/vipshop-search)
- [Vipshop](https://www.vip.com/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown tables or plain text summaries derived from JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output is paginated with up to 10 products per request and may include product links, images, prices, discounts, brands, and detail-query prompts.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
