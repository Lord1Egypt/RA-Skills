## Description: <br>
ShopMind Price Compare helps agents search prices, coupons, hot products, savings, and purchase links across Taobao/Tmall, JD.com, Pinduoduo, Douyin, Kuaishou, Suning, Vipshop, Kaola, and 1688. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohaook](https://clawhub.ai/user/xiaohaook) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shopping users and agents use this skill to compare product prices, find coupon-backed offers, inspect hot products, and generate purchase links from supported Chinese e-commerce marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping search terms and product lookups are sent to maishou88.com. <br>
Mitigation: Review network use before installing and avoid entering sensitive shopping queries. <br>
Risk: Generated purchase links may include invite or share identifiers and may not be neutral. <br>
Mitigation: Verify prices, coupons, and destination links directly with the merchant before buying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaohaook/shopmind-price-compare) <br>
- [Skill homepage](https://clawhub.com/skills/shopmind-price-compare) <br>
- [Publisher profile](https://clawhub.ai/user/xiaohaook) <br>
- [Maishou API service](https://appapi.maishou88.com) <br>
- [Maishou share service](https://msapi.maishou88.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text with command examples and occasional JSON status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and Python >=3.8; requests product data from maishou88.com and can emit purchase links.] <br>

## Skill Version(s): <br>
2.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
