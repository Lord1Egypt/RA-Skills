## Description: <br>
Recognizes telegraphic transfer vouchers and extracts remitter, payee, account, amount, date, and bank fields from local image or PDF files through Scnet OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to send a prepared bank transfer voucher file to Scnet OCR and receive structured fields for review or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected transfer voucher files are uploaded to Scnet's OCR service for processing. <br>
Mitigation: Use this skill only when sending those documents to Scnet is approved; avoid regulated, confidential, or customer financial documents unless privacy, retention, and deletion terms are understood. <br>
Risk: The skill requires a sensitive SCNET_API_KEY credential. <br>
Mitigation: Keep the credential in the local config file or environment and do not paste it into chat. <br>
Risk: OCR output may contain financial account and payment fields that need review before downstream use. <br>
Mitigation: Have a user review extracted voucher fields before relying on them for financial, compliance, or customer-facing workflows. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md) <br>
- [Telegraphic transfer voucher output fields](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [ClawHub skill listing](https://clawhub.ai/scnet-sugon/telegraph-transfer-ocr) <br>
- [Publisher profile](https://clawhub.ai/user/scnet-sugon) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON recognition results printed to standard output, with human-readable error text for configuration, authentication, file, network, or rate-limit failures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an SCNET_API_KEY credential and uploads the selected voucher file to Scnet's OCR service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
