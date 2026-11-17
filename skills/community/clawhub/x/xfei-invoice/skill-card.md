## Description:

Recognize and extract structured data from invoices, receipts, and bills using the iFlytek OCR API, including VAT invoices, taxi receipts, train tickets, toll invoices, medical bills, and bank receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingzhe2020](https://clawhub.ai/user/qingzhe2020)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run OCR on invoice, receipt, and bill images or PDFs and return structured fields for digitization and expense workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice, receipt, medical, or financial documents are uploaded to a third-party OCR service.

Mitigation: Use only documents you are authorized to send to iFlytek, and avoid sensitive medical or financial records unless that external processing is approved.

Risk: Troubleshooting commands can print XFEI_API_KEY or XFEI_API_SECRET in a terminal or logs.

Mitigation: Do not run commands that echo secrets; if credentials were displayed in a shared or logged environment, rotate them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingzhe2020/skills/xfei-invoice)
- [iFlytek console](https://console.xfyun.cn)
- [iFlytek invoice recognition service pricing](https://www.xfyun.cn/services/Invoice_recognition?target=price)
- [iFlytek invoice recognition API endpoint](https://api.xf-yun.com/v1/private/sc45f0684)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands; script output is human-readable text or raw JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XFEI_APP_ID, XFEI_API_KEY, and XFEI_API_SECRET environment variables and sends document images or PDFs to iFlytek for OCR.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
