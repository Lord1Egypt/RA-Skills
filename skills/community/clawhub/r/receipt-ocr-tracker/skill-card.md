## Description:

Receipt OCR Tracker helps an agent run Tesseract OCR on receipt photos and convert recognized receipt lines into expense CSV output for freelancers and small businesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skunnyo](https://clawhub.ai/user/skunnyo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to process receipt images, extract dates and amounts, and prepare expense records for spreadsheet import or business tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt OCR and simple parsing can produce inaccurate or unsafe expense CSV records.

Mitigation: Inspect generated CSV rows and totals before importing them into Google Sheets or using them for business records.

Risk: Receipt images and extracted expense data may contain sensitive personal or business information.

Mitigation: Use the skill only on receipts that are acceptable to store and process locally.

Risk: The script writes an expenses.csv file in the current working directory.

Mitigation: Run it from an intended output directory and confirm it will not overwrite an important file.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CSV-oriented expense output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local receipt-derived expense data that should be reviewed before importing into spreadsheets or business records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
