## Description: <br>
Processes uploaded receipts, bills, invoices, and screenshots into categorized expense claim PDFs, an XLSX summary, currency-conversion totals, and portal-ready tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[insanelyqurious](https://clawhub.ai/user/insanelyqurious) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees preparing business travel reimbursement claims use this skill to classify receipts by TCS category, generate per-day PDF bundles and XLSX summaries, and produce manual-entry tables for expense portals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipts and invoices can contain personal, financial, travel, and employer reimbursement details. <br>
Mitigation: Use the skill only for receipts intended for claim processing and keep generated PDFs, spreadsheets, and summaries within the appropriate expense workflow. <br>
Risk: Generated claim packages may contain incorrect classifications, missing receipt details, ambiguous currencies, or stale exchange rates. <br>
Mitigation: Review all generated PDFs, spreadsheet rows, currency notes, and flagged items before submitting an expense claim. <br>
Risk: Spreadsheet output may include text extracted from untrusted receipts. <br>
Mitigation: Open generated spreadsheets cautiously and inspect suspicious receipt-derived fields before reuse or submission. <br>
Risk: Live FX lookup can expose query context and may be unnecessary for claims that can use provided or finance-approved rates. <br>
Mitigation: Avoid live FX lookup unless needed and verify exchange rates against the applicable finance policy for the travel dates. <br>


## Reference(s): <br>
- [TCS Expense Categories - Eligibility & Filing Rules](tcs_categories.md) <br>
- [Standard FX Rates Reference](fx_rates.md) <br>
- [ClawHub release page](https://clawhub.ai/insanelyqurious/tcs-expense-claim) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown tables plus generated PDF and XLSX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one PDF per day and category, an expense_claim.xlsx workbook, summary tables, currency notes, and flagged items for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
