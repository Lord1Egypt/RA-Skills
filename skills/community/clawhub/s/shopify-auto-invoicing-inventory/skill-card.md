## Description:

Lightweight Shopify order invoicing and inventory operations workflow for detecting new orders, preparing invoice-ready billing data, updating stock tables, and producing simple monthly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaelbuenobarthe](https://clawhub.ai/user/gaelbuenobarthe)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopify merchants and back-office operators use this skill to review new orders, prepare invoice-ready billing data, reconcile inventory, flag exceptions, and generate monthly operations summaries before taking external accounting or fulfillment actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports may contain spreadsheet formulas or customer-controlled values that execute when opened in spreadsheet software.

Mitigation: Inspect inputs and exports, avoid opening files with formula execution enabled, and add spreadsheet-safe escaping before using customer-controlled order or product data.

Risk: Draft invoice data or tax treatment could be mistaken for official accounting compliance.

Mitigation: Keep outputs review-first, avoid claiming invoices were sent, and require accountant review when tax treatment is uncertain.

Risk: Missing billing, SKU, currency, or stock fields can lead to incorrect invoicing or inventory updates.

Mitigation: Flag incomplete orders and negative or low stock as exceptions that require human review before external action.

## Reference(s):

- [Invoice and Report Templates](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with compact tables, CSV-ready rows, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-first outputs; generated CSV files should be inspected before business use.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
