## Description: <br>
SupplyFlow is a local manufacturing supply chain toolkit for inventory tracking, supplier evaluation, procurement workflows, demand forecasting, risk assessment, cost optimization, and supplier performance reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keybryant](https://clawhub.ai/user/keybryant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing operations, procurement, and supply-chain teams use this skill to analyze JSON inventory, supplier, purchasing, demand, risk, and cost data and produce Markdown reports or purchase-order drafts for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated purchase orders may be mistaken for approved operational orders. <br>
Mitigation: Review generated purchase orders before using them operationally. <br>
Risk: Inputs may include sensitive inventory, supplier, purchasing, or forecasting data. <br>
Mitigation: Provide only intended data and handle outputs under the same internal data controls. <br>
Risk: The advertised free and paid split is described in text but not enforced by the local scripts. <br>
Mitigation: Do not rely on the scripts for access control; enforce tiering outside the skill if needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/keybryant/supplyflow) <br>
- [Supply Chain Metrics and Formulas](references/metrics.md) <br>
- [Industry Benchmarks](references/benchmarks.md) <br>
- [Purchase Order Templates](references/po_templates.md) <br>
- [Supplier Evaluation Criteria](references/supplier_criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and tables, with optional JSON output from supported scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts accept JSON input through command-line arguments or files and run locally without external API dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
