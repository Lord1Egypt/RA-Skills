## Description: <br>
Calls Tencent Cloud's VatInvoiceOCR API to extract full-field structured data from VAT invoice images or PDFs, including invoice identifiers, dates, buyer and seller details, amounts, tax fields, line items, and related metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to send VAT invoice images, PDFs, or invoice URLs to Tencent Cloud OCR and receive structured invoice fields for extraction, validation, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice images, PDFs, or URLs are sent to Tencent Cloud for OCR processing. <br>
Mitigation: Use the skill only when authorized to process the target invoices through Tencent Cloud, and avoid sending documents whose tax IDs, bank details, addresses, or line items must remain local. <br>
Risk: The skill requires Tencent Cloud credentials and may incur OCR API charges. <br>
Mitigation: Use dedicated least-privilege Tencent Cloud keys, keep credentials out of source control, and monitor API usage and billing. <br>


## Reference(s): <br>
- [Tencent Cloud VatInvoiceOCR API documentation](https://cloud.tencent.com/document/api/866/36210) <br>
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-vatinvoice) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [JSON with formatted invoice fields by default, or raw Tencent Cloud OCR JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires either an image URL or Base64/file input; PDF processing requires the PDF flag and an optional page number.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
