## Description: <br>
在唯品会搜索商品、比价和查找折扣，并通过 Python 脚本返回商品名称、品牌、价格、折扣、原价和链接等结构化结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vip](https://clawhub.ai/user/vip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search Vipshop products by keyword, compare prices and discounts, browse paginated results, filter by price range, and request details for a selected result. The skill requires a Vipshop login session before product search can proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a stored Vipshop login session and account tokens to perform searches and generate product links. <br>
Mitigation: Install and run it only for trusted users, review the stored session handling before use, and treat generated product links as account-sensitive. <br>
Risk: The skill can install or run login-related companion skills as part of its flow. <br>
Mitigation: Review the vipshop-user-login and vipshop-product-detail skills before allowing this skill to install or invoke them. <br>
Risk: Server security evidence marks the release as suspicious because of login-session behavior, even though no specific risk findings were listed. <br>
Mitigation: Require explicit operator approval before deployment and monitor execution involving stored credentials or generated login links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vip/vip-product-search) <br>
- [Vipshop website](https://www.vip.com/) <br>
- [Vipshop product search API endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/search/product/rank) <br>
- [Vipshop product detail API endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/product/module/list/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [JSON from scripts, formatted as Markdown tables or plain text for users] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 10 products per page and may include account-sensitive product links derived from the user's Vipshop login session.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
