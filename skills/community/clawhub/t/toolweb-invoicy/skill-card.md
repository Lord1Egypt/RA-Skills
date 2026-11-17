## Description:

Generate, download, and email professional invoices with GST/IGST support and flexible payment terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and business software teams use this skill to generate invoice records, calculate GST/IGST tax totals, download invoice PDFs, and send invoices by email through an API workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice generation and email delivery may require sending invoice contents, customer details, tax identifiers, bank/payment fields, and SMTP credentials to a third-party service.

Mitigation: Use only data approved for ToolWeb processing, avoid reusable mailbox passwords, prefer a dedicated low-privilege sending account or app-specific SMTP credential, and rotate any SMTP password already submitted through this service.

Risk: The server security evidence reports a suspicious verdict because the artifact does not provide enough disclosure or handling safeguards for sensitive invoice and email data.

Mitigation: Review data-handling expectations before deployment, test with non-sensitive data first, and require internal approval before processing real customer, tax, payment, or mailbox credential data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-invoicy)
- [ToolWeb Invoicy API Route](https://api.toolweb.in/tools/invoicy)
- [Invoicy API Docs](https://api.toolweb.in:8165/docs)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [JSON responses with optional PDF invoice downloads and email delivery status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process invoice contents, customer details, tax identifiers, bank or payment fields, and SMTP credentials supplied by the caller.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
