## Description:

E-commerce warehouse and inventory optimization advisor that analyzes inventory health, calculates safety stock and reorder points, performs ABC analysis, evaluates fulfillment costs, and provides actionable recommendations for improving efficiency across major fulfillment models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators and business teams use this skill to audit warehouse, inventory, and fulfillment operations, then receive calculations and prioritized recommendations for reducing stockouts, overstock, and fulfillment costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command runs unpinned remote software and installs globally.

Mitigation: Review or replace the install command before use; prefer a pinned CLI version, immutable skill source, and non-global installation.

Risk: Warehouse, marketplace, and fulfillment benchmark figures may become stale or differ from current platform fee schedules.

Mitigation: Verify business-critical calculations against current marketplace, carrier, 3PL, and internal system data before acting.

Risk: The skill cannot access real-time inventory systems, WMS data, or marketplace APIs.

Mitigation: Provide current operational data manually and treat recommendations as decision support rather than live system state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phheng/skills/warehouse-optimization)
- [Publisher Profile](https://clawhub.ai/user/phheng)
- [Nexscope](https://www.nexscope.ai/)
- [Amazon Skills](https://github.com/nexscope-ai/Amazon-Skills)
- [eCommerce Skills](https://github.com/nexscope-ai/eCommerce-Skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with tables, calculations, recommendations, and occasional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key required; relies on user-provided operational data and static guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
