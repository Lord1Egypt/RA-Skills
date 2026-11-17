## Description:

A script-driven skill for French accounting firms that reconciles invoices with bank-statement transactions, validates VAT, and summarizes follow-up, reminder, anomaly, and batch-report JSON files for accountant review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

French accounting firms and accountants use this skill to run daily reconciliation over already organized client folders and review paid, unpaid, partial, and overdue invoices, VAT issues, reminder candidates, and blocking anomalies.

### Deployment Geography for Use:

France

## Known Risks and Mitigations:

Risk: The matching code can incorrectly mark invoices as paid, which may affect closing, reminders, or client decisions.

Mitigation: Use the generated paid, unpaid, partial, and overdue results only after human accountant review, and do not rely on them for closing or reminders until the matching issues are fixed.

Risk: Running the skill against the wrong or unreviewed client root can produce misleading accounting reports.

Mitigation: Install it only for the intended French accounting workflow and first run it on a test copy or a reviewed client root.

## Reference(s):

- [CSV reconciliation schema](references/csv-schema.md)
- [Transaction-to-invoice matching rules](references/matching-rules.md)
- [Target folder structure and naming conventions](references/structure-cible.md)
- [organisation-documents companion skill](https://github.com/developers-trendex/organisation-documents)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown summary with generated JSON reconciliation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-client followup.json, relances.json, anomalies.json, and a consolidated compta_batch_report_<date>.json for accountant review.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
