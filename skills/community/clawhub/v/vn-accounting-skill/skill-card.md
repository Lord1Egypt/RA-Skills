## Description: <br>
Process accounting documents, including invoices, purchase orders, and bank statements, by extracting structured data from PDFs and images with OCR and producing Excel tracking sheets and JSON backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DVNghiem](https://clawhub.ai/user/DVNghiem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and accounting teams use this skill to classify accounting documents, extract invoice, purchase order, and bank statement fields, and prepare structured outputs for review and tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented batch workflow can execute attacker-controlled shell commands through eval when processing classifier output. <br>
Mitigation: Do not use the README eval batch snippet on untrusted files; use --classify-only or route by the returned document type with fixed script calls and quoted arguments. <br>
Risk: The skill writes extracted accounting data to Excel and JSON files, which may contain sensitive financial information. <br>
Mitigation: Store generated Excel and JSON files only in protected locations and use --dry-run when persistent outputs are not needed. <br>


## Reference(s): <br>
- [Accounting Skill on ClawHub](https://clawhub.ai/DVNghiem/vn-accounting-skill) <br>
- [Invoice Field Reference](references/invoice-fields.md) <br>
- [Bank Statement Formats](references/bank-formats.md) <br>
- [Purchase Order Field Reference](references/po-fields.md) <br>
- [OCR Setup Guide](references/ocr-setup.md) <br>
- [PEP 723 Inline Script Metadata](https://peps.python.org/pep-0723/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, Excel files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts produce JSON responses, JSON backup files, and Excel workbooks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run parsing, confidence scores, validation alerts, and configurable Excel and JSON output paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
