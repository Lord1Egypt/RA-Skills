## Description: <br>
Receipt OCR Tracker helps an agent run a local Python OCR workflow that extracts receipt text with Tesseract and writes parsed expense data to CSV for review or import into spreadsheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skunnyo](https://clawhub.ai/user/skunnyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, freelancers, and small-business operators use this skill to process receipt images into expense CSV output and a short human-readable summary. Developers and agents can also use it as local command guidance for running the bundled OCR script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt images and parsed expenses may contain sensitive personal or business information. <br>
Mitigation: Run the OCR workflow locally, keep generated CSV files in an appropriate directory, and redact or review output before sharing or importing it into external tools. <br>
Risk: The OCR script writes expenses.csv in the current working directory, which can overwrite an existing file with the same name. <br>
Mitigation: Run the script in a working directory where replacing expenses.csv is acceptable, or rename existing files before execution. <br>
Risk: OCR and regex parsing can produce inaccurate dates, items, amounts, taxes, or totals, especially for blurry receipts. <br>
Mitigation: Review the CSV and Markdown summary against the original receipt before using the data for accounting, reimbursement, or tax records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skunnyo/receipt-ocr-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands plus local CSV output from the OCR script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script writes expenses.csv in the current working directory and prints a short text sample.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
