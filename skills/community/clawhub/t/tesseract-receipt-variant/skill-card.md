## Description: <br>
Tesseract Receipt Tracker helps agents OCR receipts, invoices, and receipt images, extract common expense fields, and prepare structured JSON or CSV logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skunnyo](https://clawhub.ai/user/skunnyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who track expenses, travel, tax records, or freelance receipts can use this skill to OCR receipts or invoices and extract fields such as date, vendor, total, tax, mileage, items, category, and notes for structured logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill setup asks the agent to install Tesseract with privileged system package commands. <br>
Mitigation: Review setup before use; install Tesseract manually when possible, or approve package installation only in a controlled environment. <br>
Risk: OCR and regex parsing can misread or miss receipt fields such as totals, taxes, mileage, dates, vendors, or items. <br>
Mitigation: Review extracted JSON or CSV records against the source receipt before relying on them for expense, tax, reimbursement, or travel records. <br>


## Reference(s): <br>
- [Receipt Extraction Fields](references/receipt_fields.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/skunnyo/tesseract-receipt-variant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, CSV, Shell commands, Files] <br>
**Output Format:** [OCR text plus structured JSON or CSV expense records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append local receipt logs such as expense_log.csv or JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
