## Description: <br>
Provides tools for browsing Taobao Tiantian deals, including paginated product lists, sorting, product details, coupons, purchase links, and channel statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Shopping assistants and agents use this skill to browse current Taobao Tiantian deal listings, compare sort orders, retrieve product details, and present coupon or purchase links to users. It supports deal discovery only and does not place orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product lookup requests are sent through the publisher's Tencent Cloud proxy before reaching Taobao-related APIs. <br>
Mitigation: Use the skill only for intended Taobao deals browsing and avoid sending sensitive personal information in lookup prompts. <br>
Risk: The publisher's proxy token is disclosed in the submitted artifact. <br>
Mitigation: Publisher should rotate and protect the proxy token; users should install only versions whose publisher they trust. <br>
Risk: Shopping information, coupons, stock, and prices may change after retrieval. <br>
Mitigation: Confirm final price, coupon rules, inventory, and seller information on the destination Taobao page before purchasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/taobao-tiantian) <br>
- [Publisher profile](https://clawhub.ai/user/cn-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON strings containing product data and concise human-facing summaries suitable for agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Product data may include item titles, brand and shop names, category, prices, coupon information, promotional labels, image URLs, buy links, coupon links, pagination state, cache status, and category statistics.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
