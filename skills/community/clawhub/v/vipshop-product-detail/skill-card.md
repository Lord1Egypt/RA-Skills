## Description: <br>
Queries Vipshop product details by product ID or product link and returns structured shopping information after the user has logged in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viphgta](https://clawhub.ai/user/viphgta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to retrieve Vipshop product images, prices, discounts, service tags, authenticity information, reviews, and product links from a product identifier. The skill expects a saved Vipshop login and may invoke a companion login flow before querying product data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads saved Vipshop login tokens and can create chat-visible exchange-token links that function as sensitive login material. <br>
Mitigation: Install and run it only for users who accept this behavior, and do not share generated exchange-token links or leave them in public logs. <br>
Risk: The skill can automatically install or run the companion Vipshop login skill when no valid login is present. <br>
Mitigation: Review the companion login skill and confirm the login flow before allowing automatic installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/viphgta/vipshop-product-detail) <br>
- [Vipshop product detail API endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/detail/main/v6) <br>
- [Vipshop exchange-token endpoint](https://passport.vip.com/exchangeTokenFromApp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON, Shell commands] <br>
**Output Format:** [JSON from the script, usually reformatted by the agent as Markdown or plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product image URLs and an auto-login exchange-token product link when a valid Vipshop login token is available.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
