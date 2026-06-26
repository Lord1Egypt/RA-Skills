## Description: <br>
Generate, download, and email professional invoices with GST/IGST support and flexible payment terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and businesses use Invoicy to automate invoice creation, retrieval, and email delivery for e-commerce, SaaS billing, accounting, and freelance billing workflows. It supports line items, tax calculations, payment terms, multi-currency invoices, and Indian GST/IGST fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice payloads can contain sensitive business, customer, tax, bank, and payment details that are sent to an external provider and may be retained for later retrieval. <br>
Mitigation: Use only data approved for this provider, minimize bank and tax details where possible, and confirm the provider's retention, deletion, and access-control practices before production use. <br>
Risk: The email endpoint accepts SMTP usernames and passwords. <br>
Mitigation: Use test or limited app-specific SMTP credentials, rotate credentials regularly, and avoid sharing broad mailbox passwords. <br>
Risk: Invoices can be emailed directly to recipients. <br>
Mitigation: Confirm recipient addresses, invoice contents, and payment details before sending. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-invoicy) <br>
- [OpenAPI Schema](artifact/openapi.json) <br>
- [Invoicy API Route](https://api.toolweb.in/tools/invoicy) <br>
- [API Docs](https://api.toolweb.in:8165/docs) <br>


## Skill Output: <br>
**Output Type(s):** [JSON responses, PDF files, email delivery status, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples; API responses are JSON and generated invoices can be downloaded as PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The email endpoint accepts SMTP connection settings and returns delivery status metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
