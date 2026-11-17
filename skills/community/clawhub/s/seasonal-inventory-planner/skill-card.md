## Description:

Build month-by-month inventory plans that align purchasing, stocking, and markdown timing with seasonal demand curves to prevent both stockouts during peaks and overstock during troughs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operators, inventory planners, and purchasing teams use this skill to turn historical seasonal sales patterns into actionable inventory calendars with reorder dates, quantity targets, safety stock, cash-flow timing, and markdown triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Planning may require commercial inventory, revenue, supplier, and cash-flow details.

Mitigation: Share only data approved for planning use with the agent, and redact supplier or financial details that are not needed for the inventory plan.

Risk: Inventory recommendations can be misleading when historical demand data is incomplete, affected by stockouts, or distorted by promotions.

Mitigation: Use the quality checklist to validate data coverage, stockout adjustments, promotion flags, and confidence intervals before acting on the plan.

Risk: Long supplier lead times can force purchase commitments before reliable demand signals are available.

Mitigation: Document blind-buy assumptions, concentrate early commitments on proven products, reserve budget for later top-ups, and define markdown triggers before the season starts.

## Reference(s):

- [Seasonal Inventory Planner on ClawHub](https://clawhub.ai/leooooooow/skills/seasonal-inventory-planner)
- [Seasonal Inventory Plan Output Template](references/output-template.md)
- [Seasonal Decomposition Guide](references/seasonal-decomposition.md)
- [Post-Season Playbook](references/post-season-playbook.md)
- [Seasonal Inventory Plan Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with structured tables, checklists, and planning recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces forecast, inventory target, reorder, cash-flow, markdown, risk, and next-step planning sections.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
