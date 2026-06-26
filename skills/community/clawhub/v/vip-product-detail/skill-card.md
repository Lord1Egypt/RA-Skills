## Description: <br>
查询唯品会商品详情，并根据商品ID或商品链接汇总价格、折扣、图片、服务保障、正品信息、用户评价和商品链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vip](https://clawhub.ai/user/vip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Vipshop shoppers and shopping assistants use this skill to retrieve structured product details for a specific item and present them as a concise Markdown summary. It is useful when comparing prices, discounts, service guarantees, images, reviews, and purchase links for a Vipshop product. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Vipshop login tokens from the user's home directory and sends session cookies to Vipshop. <br>
Mitigation: Install and run it only when comfortable sharing a Vipshop session with the skill, and review the security guidance before use. <br>
Risk: The skill can install or invoke a separate login helper. <br>
Mitigation: Confirm the login helper source and behavior before allowing the automated login flow. <br>
Risk: Generated exchange-token links may contain sensitive session material. <br>
Mitigation: Do not share generated auto-login or exchange-token links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vip/vip-product-detail) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary derived from JSON product data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Vipshop product ID or product link and a valid Vipshop login session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
