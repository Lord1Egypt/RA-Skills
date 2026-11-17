## Description:

自动化差旅费用报销流程，支持12306火车票、携程机票/酒店、华住会酒店、美团、吉祥航空、百望等电子发票的自动获取、解析和报销提交。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sangjie123](https://clawhub.ai/user/sangjie123)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and finance operations users use this skill to collect travel invoices from email attachments or invoice links, extract invoice and itinerary details, prepare reimbursement records, upload invoices to FOL, and submit travel expense claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox access can expose unrelated or sensitive messages when filters are too broad.

Mitigation: Use narrow date, sender, and subject filters and confirm the mailbox scope before searching or downloading invoice messages.

Risk: Invoice links from email may point to untrusted or unexpected files.

Mitigation: Allowlist expected invoice domains and validate downloaded file type, filename, and size before processing.

Risk: Automated FOL upload and reimbursement submission can create financial records before the user has reviewed them.

Mitigation: Require explicit user confirmation before invoice upload and again before final reimbursement submission.

Risk: Local processing stores personal travel and invoice data in working directories.

Mitigation: Define retention and deletion rules for downloaded invoices, OCR text, itinerary files, and reimbursement outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sangjie123/skills/travel-expense-reimbursement)
- [差旅费用报销流程图](references/flowchart.md)
- [OCR发票解析指南](references/ocr-guide.md)
- [行程分析指南](references/行程分析指南.md)
- [url_downloader.py](references/url_downloader.py)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summaries, JSON reimbursement data, file paths, and guided shell or browser actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local invoice, itinerary, and reimbursement files and may drive browser-based FOL upload and submission steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
