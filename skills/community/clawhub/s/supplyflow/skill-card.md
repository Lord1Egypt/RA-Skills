## Description:

Manufacturing supply chain management toolkit for inventory tracking, supplier evaluation, procurement workflows, demand forecasting, risk assessment, cost optimization, and supplier performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keybryant](https://clawhub.ai/user/keybryant)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing supply chain teams and developers use this skill to run local analyses for inventory levels, supplier scoring, purchase orders, demand forecasts, risk assessment, cost optimization, and supplier performance reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports from supplier, procurement, inventory, or forecast data may contain misleading calculations or recommendations if the input data is incomplete or untrusted.

Mitigation: Review source data and validate calculations before using outputs for purchasing, supplier, inventory, or cost decisions.

Risk: Markdown reports generated from untrusted business data may carry normal presentation-layer risks when copied into downstream tools.

Mitigation: Treat generated Markdown as untrusted content and review it before sharing, rendering, or importing it into other systems.

## Reference(s):

- [SupplyFlow ClawHub release](https://clawhub.ai/keybryant/skills/supplyflow)
- [供应链指标与公式](references/metrics.md)
- [行业基准数据](references/benchmarks.md)
- [采购订单模板](references/po_templates.md)
- [供应商评估标准](references/supplier_criteria.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports and tables, with optional JSON from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts accept JSON input and run locally without external API dependencies.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
