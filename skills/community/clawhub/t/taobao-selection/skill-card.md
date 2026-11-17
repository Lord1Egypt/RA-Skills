## Description:

淘宝天猫好货搜索比价领券，标品按到手价排序找最低价，非标品按销量排序找口碑好货，自动筛选包邮+消保+高评分商品，返回优惠券和购买链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to search Taobao and Tmall product listings, compare standard items by final price, and find lifestyle items by sales and reputation signals. It returns product summaries, coupon information, price filters, pagination, and purchase links, but it does not place orders or check logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged release exposes a reusable proxy token.

Mitigation: Remove the embedded token, rotate it before release, and require secure runtime configuration for proxy credentials.

Risk: Shopping queries are sent through a proxy service and the proxy destination can be externally configured.

Mitigation: Review the proxy destination before installation, restrict allowed destinations, and avoid sending sensitive personal information in search terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/taobao-selection)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Text product listings with prices, coupons, sales counts, shop names, categories, and purchase links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns search results for one requested page at a time; no ordering, logistics, or price-alert actions are performed.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
