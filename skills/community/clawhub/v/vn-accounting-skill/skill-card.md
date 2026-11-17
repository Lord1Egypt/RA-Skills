## Description:

Process accounting documents, including invoices, purchase orders, and bank statements, by classifying files and extracting structured data from PDFs and images with OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dvnghiem](https://clawhub.ai/user/dvnghiem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, finance operations teams, and accounting staff use this skill to extract structured records from invoices, purchase orders, and bank statements, then save tracking data as Excel workbooks and JSON backups. It is useful for Vietnamese and international accounting document workflows that need OCR, classification, confidence scoring, and validation alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review flags unsafe command-running guidance in the README batch workflow.

Mitigation: Avoid the README batch workflow that uses eval; run extractor scripts directly with quoted paths or use a safe dispatcher.

Risk: The server security review notes that untrusted document text can be written into generated Excel files.

Mitigation: Store outputs only in protected directories and be cautious when opening generated spreadsheets from untrusted documents.

Risk: The server security review recommends dependency review before installation.

Mitigation: Prefer pinned dependencies or a locked environment before running the skill.

## Reference(s):

- [Invoice Field Reference](artifact/references/invoice-fields.md)
- [Bank Statement Formats](artifact/references/bank-formats.md)
- [Purchase Order Field Reference](artifact/references/po-fields.md)
- [OCR Setup Guide](artifact/references/ocr-setup.md)
- [PEP 723 Inline Script Metadata](https://peps.python.org/pep-0723/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with shell commands; extractor scripts produce JSON records and Excel workbooks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include OCR confidence, extraction confidence, validation status, and needs-review flags.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
