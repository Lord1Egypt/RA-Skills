## Description:

淘宝好券精选 helps agents query selected Taobao and Tmall coupon products, including paginated product lists, sorting, item details, coupon information, and channel statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shopping assistants and consumer-facing agents use this skill to browse Taobao coupon selections, compare coupon-adjusted prices, retrieve product details, and summarize channel statistics before handing users off to purchase links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coupon queries are sent through the publisher's cloud proxy, and evidence.security reports an embedded proxy authentication token.

Mitigation: Install only if this proxy use is acceptable; the publisher should rotate and remove embedded tokens and move credentials to tightly scoped managed configuration.

Risk: The skill returns shopping links and coupon details that can change or differ from the final merchant page.

Mitigation: Have users verify final price, coupon threshold, and destination page before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/taobao-haoquan)
- [Publisher profile](https://clawhub.ai/user/cn-shopping)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [JSON object containing human-readable Chinese text, product links, item identifiers, prices, coupon details, image URLs, or channel statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from live proxy API responses and may include external product and image URLs.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
