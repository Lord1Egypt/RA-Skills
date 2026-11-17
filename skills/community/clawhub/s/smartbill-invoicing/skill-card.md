## Description:

Automates SmartBill.ro invoice workflows, including payload validation, invoice creation, document series listing, and invoice PDF downloads through the SmartBill API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-ai-tech](https://clawhub.ai/user/maverick-ai-tech)

### License/Terms of Use:


## Use Case:

Developers, operators, and finance teams use this skill to validate SmartBill invoice JSON, create draft or final invoices, list document series, and download invoice PDFs with local CLI checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real SmartBill credentials and invoice data can be sent to a configured API endpoint.

Mitigation: Use the default SmartBill API URL unless SMARTBILL_API_BASE or --base-url has been explicitly verified.

Risk: Debug logging can expose customer, invoice, request, or response data in stderr logs.

Mitigation: Keep SMARTBILL_DEBUG unset and avoid --debug when working with real invoice or customer data.

Risk: Creating a final invoice is a high-impact action.

Mitigation: Run validate-payload and create-invoice --dry-run first, then require explicit confirmation and --allow-final before issuing a final invoice.

Risk: Test invoice data can be saved into SmartBill contacts or product catalogs.

Mitigation: Set client.saveToDb and products[].saveToDb to false for test or one-off data.

## Reference(s):

- [SmartBill API Notes](artifact/references/smartbill-api.md)
- [Invoice Example](artifact/references/invoice-example.json)
- [SmartBill API Base URL](https://ws.smartbill.ro/SBORO/api)
- [ClawHub Skill Page](https://clawhub.ai/maverick-ai-tech/skills/smartbill-invoicing)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI responses; PDF files for invoice downloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SmartBill credentials. Final invoice creation requires explicit --allow-final.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
