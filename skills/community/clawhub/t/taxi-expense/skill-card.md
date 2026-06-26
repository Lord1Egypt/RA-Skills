## Description: <br>
Processes Didi taxi order screenshots with OCR, redacts destination details, and generates monthly reimbursement Excel files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kathi-hash](https://clawhub.ai/user/kathi-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees who submit overtime taxi reimbursement use this skill to turn original Didi order screenshots into monthly reimbursement workbooks with destination masking and reimbursable-ride filtering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Taxi dates, pickup and destination details, amounts, redacted screenshots, and spreadsheets are stored locally. <br>
Mitigation: Use the skill only when local storage of this reimbursement data is acceptable, and delete the taxi_expense outputs when they are no longer needed. <br>
Risk: Destination masking and OCR parsing can be imperfect, so generated reimbursement files may contain incorrect or insufficiently redacted details. <br>
Mitigation: Review the generated Excel workbook and screenshots before sharing or submitting them. <br>
Risk: The optional Telegram preview command can send reimbursement files to the wrong recipient if the target is incorrect. <br>
Mitigation: Confirm the Telegram recipient manually before sending any generated workbook or screenshot. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kathi-hash/taxi-expense) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Console summary plus generated XLSX workbook, JSON order data, and redacted PNG screenshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Monthly XLSX files include reimbursement details and redacted order screenshots; local JSON data is deduplicated by date and amount.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
