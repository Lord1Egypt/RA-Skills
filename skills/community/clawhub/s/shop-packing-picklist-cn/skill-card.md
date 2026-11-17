## Description:

将最多20个脱敏订单的SKU、数量、单位、已确认套装组成、赠品条件和包装规则整理为逐单拣货装箱勾选表与拆套组件汇总，适合仓配人员进行当次发货前人工核对；缺单位、套装组成或赠品适用条件时明确列为待确认，绝不猜测附件、赠品或包裹数量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

仓配人员可用此技能将脱敏订单整理成逐单拣货与装箱勾选清单，并汇总已确认套装的组件数量，以便在发货前人工核对。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 订单资料可能包含敏感业务信息。

Mitigation: 仅提供脱敏订单资料。

Risk: 不完整或有误的输入可能导致拣货清单不准确。

Mitigation: 装箱前由人员核对清单，并补齐所有待确认项。

Risk: 文档中的安装命令未固定版本。

Mitigation: 优先使用经过审查的安装器和技能版本。

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xxjrq/skills/shop-packing-picklist-cn)
- [Project repository](https://github.com/xxjrq/shop-packing-picklist-cn)
- [ERPNext Packing Slip business reference](https://github.com/frappe/erpnext/blob/develop/erpnext/stock/doctype/packing_slip/packing_slip.json)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [最多处理20个脱敏订单、100条商品或组件行；缺失单位、套装组成或赠品条件会列为待确认项。]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
