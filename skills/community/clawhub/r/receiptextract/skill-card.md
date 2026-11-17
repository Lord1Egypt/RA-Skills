## Description:

Extract structured transaction data from receipt photos, scans, and PDFs with the ReceiptExtract API, then return JSON, summaries, or CSV for downstream workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yborunov](https://clawhub.ai/user/yborunov)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract merchant, date, line-item, tax, total, and traceability fields from receipt images or PDFs. It is suited for testing ReceiptExtract on sample files and wiring receipt parsing into scripts, automations, or agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt files sent to ReceiptExtract may contain merchant, location, purchase, tax, or payment-related details.

Mitigation: Process only receipts the user is authorized to upload and avoid sending sensitive receipts unless the third-party API use is acceptable.

Risk: The ReceiptExtract API token could be exposed if pasted into chat, embedded in commands, or committed with examples.

Mitigation: Keep the token in `RECEIPTEXTRACT_API_TOKEN` or a secret manager, and never echo raw authorization headers in user-facing output.

Risk: Bulk or recursive directory processing can upload more files than intended and consume one credit per receipt.

Mitigation: Review the selected input directory and file list before running bulk mode, especially when `--recursive` is enabled.

Risk: OCR and extraction results can be incomplete or imperfect even when the API returns useful data.

Mitigation: Sanity-check currency, tax labels, totals, and suspicious line items against the visible receipt, and do not invent missing extracted data.

## Reference(s):

- [ReceiptExtract API Notes](references/api.md)
- [ReceiptExtract](https://www.receiptextract.com)
- [Receipt Upload Endpoint](https://www.receiptextract.com/api/receipt/upload)
- [ClawHub Skill Page](https://clawhub.ai/yborunov/skills/receiptextract)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; helper output can be JSON, CSV, or plain-text summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file and directory modes; bulk JSON includes processed, succeeded, failed, and per-file results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
