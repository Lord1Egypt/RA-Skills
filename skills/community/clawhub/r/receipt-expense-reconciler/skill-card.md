## Description: <br>
Parse receipts and invoices, categorize spend, detect anomalies, and produce tax-ready expense summaries for freelancers and SMB operators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers, SMB operators, and finance support teams use this skill to turn receipt, invoice, and bank or card export data into reconciled expense records, category summaries, anomaly reports, and tax-preparation checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt, invoice, and bank or card export data can contain sensitive business and personal financial information. <br>
Mitigation: Use only data you are authorized to process, remove unnecessary personal details before sharing with an agent, and review outputs before storing or distributing them. <br>
Risk: Generated expense categories, anomaly flags, and tax-ready summaries may be incomplete or incorrect for a user's jurisdiction or filing situation. <br>
Mitigation: Treat the output as operational accounting guidance, review uncertain or anomalous rows manually, and verify filing decisions with a licensed accountant or tax advisor. <br>
Risk: Low-confidence categorization or duplicate detection mistakes could affect reconciled ledgers and summaries. <br>
Mitigation: Configure the duplicate key and anomaly threshold policy for the business context, and keep a manual review queue for low-confidence categories. <br>


## Reference(s): <br>
- [Receipt and Expense Reconciler on ClawHub](https://clawhub.ai/anugotta/receipt-expense-reconciler) <br>
- [anugotta Publisher Profile](https://clawhub.ai/user/anugotta) <br>
- [Setup](artifact/setup.md) <br>
- [Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown tables, summaries, anomaly reports, and export checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided receipts, invoices, bank or card exports, accounting period, tax regime, currencies, and category chart.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
