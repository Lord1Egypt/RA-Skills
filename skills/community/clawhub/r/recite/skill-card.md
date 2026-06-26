## Description: <br>
Recite helps an agent scan receipts, invoices, images, and PDFs with the Recite Vision API, rename files by extracted date and vendor, and maintain a local bookkeeping CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rivradev](https://clawhub.ai/user/rivradev) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers, agents, and bookkeeping users can use this skill to process a folder of receipt or invoice files, extract transaction details, rename the originals, and append structured records to a CSV ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt and invoice contents are uploaded to the Recite API for extraction. <br>
Mitigation: Use this skill only when the user trusts the Recite API with the files being processed and has consent to upload that content. <br>
Risk: The skill automatically renames local files and writes a bookkeeping CSV. <br>
Mitigation: Run it on copies or backups first, use a dedicated target directory, and review the resulting filenames and CSV before relying on them. <br>
Risk: API keys and local configuration are required for operation. <br>
Mitigation: Protect the Recite API key, avoid committing configuration files, and revoke or rotate the key if it is exposed. <br>


## Reference(s): <br>
- [Recite on ClawHub](https://clawhub.ai/rivradev/recite) <br>
- [Recite API key settings](https://recite.rivra.dev/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text] <br>
**Output Format:** [Terminal status text plus renamed receipt files and a CSV ledger] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes bookkeeping_transactions.CSV in the target directory and may rename supported image or PDF files after API extraction.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
