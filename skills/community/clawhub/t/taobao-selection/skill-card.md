## Description: <br>
零配置即装即用，提供淘宝天猫商品搜索、商品详情查询和短链接生成3项工具，支持价格筛选、优惠券筛选和排序，基于淘宝官方数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping assistants use this skill to search Taobao or Tmall products, inspect item details, filter by price or coupon availability, and create Taobao short links for sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Taobao searches, item IDs, and submitted shopping links through the publisher's proxy service. <br>
Mitigation: Review the publisher and proxy documentation before installing, and avoid submitting private, account-specific, or tracking-heavy URLs unless data handling is documented. <br>
Risk: The skill uses a built-in proxy token, so requests depend on a credential controlled outside the user's environment. <br>
Mitigation: Treat the proxy as a third-party service dependency and reinstall or disable the skill if token handling, retention policy, or service ownership is unclear. <br>
Risk: Prices, coupons, and short-link availability can change after the skill returns results. <br>
Mitigation: Verify product details, coupon terms, and generated links on Taobao or Tmall before purchasing or sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/taobao-selection) <br>


## Skill Output: <br>
**Output Type(s):** [text, json] <br>
**Output Format:** [JSON envelopes containing human-readable Chinese product search results, item details, or short-link responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Taobao or Tmall product prices, coupon information, sales counts, shop names, purchase links, and generated short links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
