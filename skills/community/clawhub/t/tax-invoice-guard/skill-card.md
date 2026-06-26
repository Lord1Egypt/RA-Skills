## Description: <br>
Tax Invoice Guard helps agents extract invoice fields, detect duplicate or tampered reimbursements, verify supported invoices against tax authority sources, and generate invoice compliance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffersplind92](https://clawhub.ai/user/jeffersplind92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, reimbursement, and compliance users use this skill to screen invoices for duplicates or tampering, check authenticity and status when approved credentials and services are available, and produce audit-ready invoice compliance reports. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive invoice metadata or service credentials may cross external trust boundaries. <br>
Mitigation: Confirm which fields are sent to OCR, tax-authority, api.yk-global.com, and Feishu services before using real invoices. <br>
Risk: External service credentials may be exposed or over-scoped. <br>
Mitigation: Use a dedicated scoped API key and avoid confidential invoices unless the organization has approved the processors. <br>
Risk: Generated compliance reports can contain sensitive financial records. <br>
Mitigation: Restrict access to generated reports and handle them under the organization's financial-record controls. <br>


## Reference(s): <br>
- [Chinese Invoice Types and Field Specifications](references/invoice-types.md) <br>
- [State Tax Administration VAT Invoice Verification Platform](references/tax-api.md) <br>
- [Invoice Compliance Report Template](references/compliance-report.md) <br>
- [InvoiceGuard Changelog](references/changelog.md) <br>
- [State Tax Administration VAT Invoice Verification Platform](https://inv-veri.chinatax.gov.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, structured results, Python snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate sensitive invoice compliance reports and service-integration payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
