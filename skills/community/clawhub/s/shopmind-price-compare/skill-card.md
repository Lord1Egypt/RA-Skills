## Description:

Compares prices, coupons, savings, hot products, and purchase links across Taobao/Tmall, JD, Pinduoduo, Douyin, Kuaishou, Suning, Vipshop, Kaola, and 1688.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohaook](https://clawhub.ai/user/xiaohaook)

### License/Terms of Use:

MIT-0

## Use Case:

External shopping users and shopping assistant agents use this skill to compare product prices, coupons, sales signals, savings, and purchase links across supported Chinese e-commerce platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping searches and product IDs are sent to Maishou APIs.

Mitigation: Avoid sensitive shopping queries and review the Maishou data-sharing implications before use.

Risk: Generated purchase links may include the default invite code unless MAISHOU_INVITE_CODE is set.

Mitigation: Disclose affiliate attribution and set MAISHOU_INVITE_CODE explicitly before generating purchase links.

Risk: The skill has dependency and disclosure gaps according to the security evidence.

Mitigation: Install in a controlled environment, pin runtime dependencies, and review the script before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaohaook/skills/shopmind-price-compare)
- [Maishou app API endpoint](https://appapi.maishou88.com)
- [Maishou share API endpoint](https://msapi.maishou88.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown-like formatted text with product listings, coupon details, savings calculations, IDs, and purchase links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results and coupon or hot-product listings are limited to the first 20 returned items.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
