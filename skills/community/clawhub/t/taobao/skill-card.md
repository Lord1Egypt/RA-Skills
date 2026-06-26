## Description: <br>
Compares product prices, coupons, details, and purchase links across Chinese e-commerce platforms using maishou88.com shopping data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[al-one](https://clawhub.ai/user/al-one) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping assistants use this skill to search Chinese e-commerce platforms, compare product prices and coupons, and retrieve product details or purchase links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product searches and detail requests are sent to maishou88.com. <br>
Mitigation: Use the skill only for shopping queries that users are comfortable sharing with that third-party service. <br>
Risk: Generated purchase links may include the publisher's default invite or referral code. <br>
Mitigation: Review referral attribution before using purchase links, and set MAISHOU_INVITE_CODE when a different invite code is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/al-one/taobao) <br>
- [Publisher profile](https://clawhub.ai/user/al-one) <br>
- [maishou88 search API](https://appapi.maishou88.com/api/v1/homepage/searchList) <br>
- [maishou88 detail API](https://appapi.maishou88.com/api/v3/goods/detail) <br>
- [maishou88 target URL API](https://msapi.maishou88.com/api/v1/share/getTargetUrl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CSV text for search results and YAML text for product detail results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search supports platform source selection and pagination; detail output may include generated purchase links and copy phrases.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
