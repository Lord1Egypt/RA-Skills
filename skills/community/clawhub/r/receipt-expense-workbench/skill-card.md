## Description: <br>
Normalize receipts, reimbursement slips, and invoices into a clean expense ledger with category mapping and anomaly flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, finance operators, and agents use this skill to turn receipt text, OCR output, invoices, or reimbursement slips into an expense ledger, category summary, anomaly report, and reimbursement checklist. It is best suited for first-pass organization and review before submitting or sharing expense records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt, invoice, and reimbursement data may contain sensitive financial records. <br>
Mitigation: Provide only the fields needed for the task, use explicit input and output paths, and handle generated CSVs as sensitive files. <br>
Risk: Generated expense ledgers may contain missing, uncertain, duplicate, or suspicious entries. <br>
Mitigation: Review the ledger, anomaly report, and checklist before submitting, reimbursing, or sharing the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/receipt-expense-workbench) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Expense ledger helper script](artifact/scripts/expense_ledger.py) <br>
- [Expense categories resource](artifact/resources/expense_categories.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated CSV-style expense ledger content, category summaries, anomaly reports, and reimbursement checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled helper script writes a local CSV from a user-provided JSON list and explicit output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
