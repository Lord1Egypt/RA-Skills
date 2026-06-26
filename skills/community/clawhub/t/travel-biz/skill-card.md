## Description: <br>
Travel Biz helps business travelers plan trips, record expenses, scan receipts or invoices, and generate reimbursement documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeman88-tch](https://clawhub.ai/user/freeman88-tch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external business travelers use this skill to coordinate business trips, track reimbursable expenses, manage receipts and invoices, and prepare reimbursement exports for finance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store business travel, receipt, invoice, and reimbursement records locally under ~/travel-biz/. <br>
Mitigation: Use approved local storage, review generated records before sharing, and avoid placing unnecessary sensitive data in trip folders. <br>
Risk: Upload, OCR, calendar sync, booking, or export workflows may pass data to companion skills or external services. <br>
Mitigation: Confirm which service receives the data before use and grant only the credentials needed for the specific task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freeman88-tch/travel-biz) <br>
- [Publisher profile](https://clawhub.ai/user/freeman88-tch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown trip plans, expense records, reimbursement forms, reports, and export instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May organize local trip records under ~/travel-biz/ and handle uploaded receipt or invoice data when companion skills are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
