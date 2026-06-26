## Description: <br>
Lightweight Shopify order invoicing and inventory operations workflow for detecting new orders, preparing invoice-ready billing data, updating stock tables, and producing simple monthly summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaelbuenobarthe](https://clawhub.ai/user/gaelbuenobarthe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Shopify merchants and operators use this skill to review orders, prepare invoice-ready billing rows, reconcile stock after sales, and produce monthly operations summaries before taking external accounting or fulfillment action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow processes Shopify order, billing, tax, and customer contact data. <br>
Mitigation: Use only data the operator is authorized to process and store generated invoice and report files in protected locations. <br>
Risk: Bundled scripts create or overwrite CSV files at user-supplied output paths. <br>
Mitigation: Review output paths before running scripts and write exports to a controlled working directory. <br>
Risk: Draft invoice rows and stock changes may be incomplete or inaccurate when source order, tax, billing, SKU, or refund data is missing. <br>
Mitigation: Keep the skill's review-first workflow: flag exceptions, avoid inventing tax data, and have a qualified reviewer confirm uncertain invoice or tax treatment before external use. <br>


## Reference(s): <br>
- [Invoice and report templates](artifact/references/templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/gaelbuenobarthe/shopify-auto-invoicing-inventory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables, CSV-ready rows, and local CSV files produced by bundled Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review-first outputs; generated invoice, inventory, and report files may contain customer billing, tax, and order data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
