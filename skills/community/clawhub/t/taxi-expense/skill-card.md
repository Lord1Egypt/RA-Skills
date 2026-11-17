## Description:

Taxi Expense processes Didi taxi order screenshots with OCR, masks destination details, filters reimbursable weekday rides after 21:00, and generates monthly reimbursement spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kathi-hash](https://clawhub.ai/user/kathi-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to process Didi taxi screenshots, redact destination details, and produce monthly Excel reimbursement records for eligible weekday evening rides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Taxi screenshots, JSON records, and spreadsheets can contain sensitive trip dates, times, locations, amounts, and receipt images.

Mitigation: Keep generated records local, restrict sharing, review spreadsheets and screenshots before distribution, and delete retained records when they are no longer needed.

Risk: Destination masking can silently fail or leave enough visible context to identify a trip destination.

Mitigation: Manually inspect redacted screenshots and Excel destination fields before reimbursement submission or external sharing.

Risk: Setup downloads Node dependencies and OCR trained data that evidence.security says should be reviewed before production use.

Mitigation: Run setup without elevated privileges and use updated, pinned dependencies plus verified OCR model files for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kathi-hash/skills/taxi-expense)
- [Tesseract OCR trained data source](https://github.com/tesseract-ocr/tessdata)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Console text plus JSON records, PNG screenshots, and Excel spreadsheets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files include monthly reimbursement workbooks, local order data, and desensitized screenshot images.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
