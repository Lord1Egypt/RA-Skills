## Description:

Tesseract Receipt Tracker uses Tesseract OCR and receipt parsing to extract expense fields such as date, vendor, total, tax, mileage, and items from receipt, invoice, and image inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skunnyo](https://clawhub.ai/user/skunnyo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to OCR receipt or invoice images and produce structured expense records for travel, freelance, tax, and mileage logging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run unpinned package installs and a privileged system package install.

Mitigation: Review before installing, install Tesseract through the normal administrator-approved process, and avoid allowing an agent to run sudo apt or unpinned pip installs automatically.

Risk: The included parser may produce limited JSON rather than full receipt or invoice tracking output.

Mitigation: Validate extracted fields against the source receipt and treat generated JSON or CSV as a draft record before using it for expense, tax, or mileage records.

## Reference(s):

- [Receipt Extraction Fields](references/receipt_fields.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown instructions with inline shell commands and JSON or CSV output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured expense records depend on OCR quality and parser field coverage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
