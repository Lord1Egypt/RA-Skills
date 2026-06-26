## Description: <br>
Extracts structured transaction data from receipt images or PDFs using the ReceiptExtract API, with JSON, CSV, and summary outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yborunov](https://clawhub.ai/user/yborunov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to upload receipt photos, scans, or PDFs to ReceiptExtract and return merchant, date, item, tax, and total data for review or downstream automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt images and PDFs can contain sensitive purchase history, addresses, timestamps, loyalty data, and payment details, and the skill uploads selected files to ReceiptExtract. <br>
Mitigation: Review ReceiptExtract privacy and retention terms before use, upload only intended files, and use narrow input paths for bulk processing. <br>
Risk: The ReceiptExtract API token could be exposed if pasted into chat, committed to source control, or printed in command output. <br>
Mitigation: Store RECEIPTEXTRACT_API_TOKEN in an environment variable or secret manager and avoid echoing tokens or raw authorization headers. <br>
Risk: OCR and parsing results may be incomplete or inaccurate for some receipts. <br>
Mitigation: Sanity-check extracted totals, taxes, currencies, and line items against the original receipt before relying on the output. <br>


## Reference(s): <br>
- [ReceiptExtract API Notes](references/api.md) <br>
- [ReceiptExtract](https://www.receiptextract.com) <br>
- [ReceiptExtract upload endpoint](https://www.receiptextract.com/api/receipt/upload) <br>
- [ClawHub skill page](https://clawhub.ai/yborunov/receiptextract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, CSV, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output can be JSON, CSV, or plain-text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-file and bulk receipt processing; bulk mode preserves per-file status and error details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
