## Description: <br>
Identifies unaccounted inventory loss in restaurant operations by cross-referencing sales volume against theoretical recipe yields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blake27mc](https://clawhub.ai/user/blake27mc) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
Restaurant and franchise operators use this skill to investigate item-level inventory variance by comparing POS sales, recipe yields, inventory counts, deliveries, and waste records. It helps identify likely causes such as over-portioning, unrecorded waste, prep errors, delivery discrepancies, or theft without requiring an inventory management integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inventory variance analysis may produce incorrect conclusions when sales counts, recipe yields, inventory counts, delivery quantities, costs, or waste logs are incomplete or inaccurate. <br>
Mitigation: Review the operator-provided numbers, document assumptions, and treat the report as a decision-support artifact before changing purchasing, staffing, or disciplinary processes. <br>
Risk: Theft is included as a possible cause, which could lead to sensitive personnel or operational decisions if handled without context. <br>
Mitigation: Present theft only as a data-backed possibility, avoid naming or accusing individuals, and require human review before acting on the conclusion. <br>
Risk: The skill may handle sensitive business data such as sales volume, food costs, vendor deliveries, and waste records. <br>
Mitigation: Use the skill only in environments approved for restaurant operating data and avoid sharing unnecessary store, employee, vendor, or financial details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blake27mc/qsr-ghost-inventory-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown investigation report with calculations, probable cause, recommended action, and follow-up date] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses operator-provided sales, recipe yield, inventory, delivery, cost, and waste inputs; no external system integration is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
