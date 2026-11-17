## Description:

Calls Tencent Cloud VatInvoiceOCR to extract full-field VAT and electronic invoice data from invoice images or PDFs and return structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to submit invoice images, invoice PDFs, or invoice URLs to Tencent Cloud OCR and extract structured VAT invoice fields such as invoice numbers, buyer and seller details, amounts, taxes, and line items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice images, PDFs, URLs, and extracted billing fields are sent to Tencent Cloud for OCR processing.

Mitigation: Install and run only when that data transfer is acceptable for the invoice data involved.

Risk: Tencent Cloud credentials are required to call the OCR service.

Mitigation: Provide credentials through environment variables with only the permissions needed for OCR, and avoid embedding secrets in prompts, files, or command history.

Risk: The skill depends on the Tencent Cloud Python SDK at runtime.

Mitigation: Use a virtual environment and consider pinning the Tencent SDK version for reproducible deployments.

## Reference(s):

- [Tencent Cloud VatInvoiceOCR API documentation](https://cloud.tencent.com/document/api/866/36210)
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/skills/tencentcloud-ocr-vatinvoice)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [JSON printed to stdout, either formatted invoice fields by default or the raw Tencent Cloud response when --raw is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials in environment variables and accepts image URL, Base64, or local file input; PDF recognition requires the PDF option.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
