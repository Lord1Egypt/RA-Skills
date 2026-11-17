## Description:

淘宝天天特卖频道商品查询，100%天猫品牌店精选，涵盖家居日用、洗护清洁、零食粮油等全品类，价格多在5-30元，支持销量/价格/热度4种排序。夏日特卖好物，淘宝天天低价精选

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-shopping](https://clawhub.ai/user/cn-shopping)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping-assistant agents use this skill to browse Taobao Tiantian Temai deals, sort deal lists by sales, price, or recommendation heat, inspect item details, and retrieve channel statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Taobao deal requests through a publisher-operated cloud proxy, so requests and outbound shopping-link retrieval depend on that remote service.

Mitigation: Install only when that proxy dependency is acceptable, and review the publisher profile and skill page before deployment.

Risk: ClawHub security evidence reports an embedded shared proxy token and configurable proxy URL, which could enable proxy abuse or unintended token disclosure.

Mitigation: Rotate or replace shared tokens, remove source-code token fallbacks, and restrict the allowed proxy host before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/taobao-tiantian)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [JSON tool responses containing human-readable Chinese text and shopping links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns paginated deal lists, single-item details, or channel statistics; item output may include image URLs and outbound purchase links.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
