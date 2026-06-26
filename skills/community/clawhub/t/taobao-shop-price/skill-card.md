## Description: <br>
Searches Chinese e-commerce marketplaces for products, compares prices and sales signals, ranks options, and returns purchase links after user selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xchicky](https://clawhub.ai/user/xchicky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping-assistant agents use this skill to search Taobao/Tmall, JD.com, Pinduoduo, Douyin, Kuaishou, 1688, and related Chinese e-commerce platforms, then compare price, coupon, sales, and relevance signals. The skill presents ranked Markdown tables and retrieves purchase links only after the user chooses products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping searches and selected product identifiers are sent to maishou88.com. <br>
Mitigation: Use the skill only when the user is comfortable sharing shopping queries and selected product identifiers with that service. <br>
Risk: Returned purchase or share links may include service identifiers or referral attribution that is not clearly disclosed. <br>
Mitigation: Disclose that links come from the external service and tell users to verify seller, destination, final price, and terms before buying. <br>
Risk: Prices, coupons, sales counts, and availability are point-in-time shopping data and may change before checkout. <br>
Mitigation: Present comparison results as current estimates and remind users to confirm price, coupon eligibility, seller, and product details at checkout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xchicky/taobao-shop-price) <br>
- [Publisher profile](https://clawhub.ai/user/xchicky) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and concise text with shell command snippets and plain-text purchase links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include parsed product listings, recommendation ratings, price/coupon/sales summaries, and purchase or share links.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
