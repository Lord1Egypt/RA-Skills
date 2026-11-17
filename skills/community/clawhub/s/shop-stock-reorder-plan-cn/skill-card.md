## Description:

面向中文小店、小说作者及自媒体创作者，把最多100行库存、近段销量、提前期和目标库存表整理为逐SKU补货建议、可复核公式依据与缺失字段清单；适合有限表格的日常补货判断，不用于订单发货、仓储软件部署或编造缺料数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as Chinese-speaking small-shop operators, writers, and independent creators can turn a limited inventory table into per-SKU reorder suggestions, formula explanations, and a list of missing fields for review before purchasing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete or inaccurate inventory fields can lead to poor reorder suggestions.

Mitigation: Provide only the fields needed for the calculation and review quantities before purchasing; the skill produces recommendations and does not place orders.

## Reference(s):

- [Package source repository (manifest link)](https://github.com/xxjrq/shop-stock-reorder-plan-cn)
- [ERPNext project (scope reference)](https://github.com/frappe/erpnext)
- [ERPNext README (scope reference)](https://github.com/frappe/erpnext/blob/develop/README.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown table with per-SKU recommendations, formula notes, risks, and missing-field details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are based on user-provided inventory data; incomplete rows are identified without inventing values.]

## Skill Version(s):

1.0.1 (source: manifest.yaml, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
