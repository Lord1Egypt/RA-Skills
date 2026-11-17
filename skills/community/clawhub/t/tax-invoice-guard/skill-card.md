## Description:

Tax Invoice Guard helps agents extract invoice fields, detect duplicate or suspicious reimbursements, check tax-verification status when configured, and generate invoice compliance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersplind92](https://clawhub.ai/user/jeffersplind92)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations teams use this skill to process invoices for reimbursement screening, duplicate detection, optional tax-status checks, and Markdown or Feishu compliance reporting.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles sensitive invoice data while the security scan reports under-disclosed credential and invoice-data handling.

Mitigation: Install only after publisher and workflow review; do not use confidential invoices until data handling, API-key checks, raw OCR output, local paths, and Feishu or tax-authority sharing are explicitly documented.

Risk: Tax-authority verification claims may be overstated when actual verification is not implemented or visible in the output.

Mitigation: Treat generated reports as unverified unless tax-authority verification is implemented and shown; manually verify invoices before reimbursement or tax decisions.

Risk: Unchecked invoices may be presented in reports in a way that readers could interpret as normal.

Mitigation: Require reports to clearly distinguish unchecked status from normal status and block acceptance of unchecked invoices as verified.

## Reference(s):

- [Chinese Invoice Types and Field Specifications](references/invoice-types.md)
- [State Tax Administration VAT Invoice Verification Platform](references/tax-api.md)
- [Invoice Compliance Report Template](references/compliance-report.md)
- [InvoiceGuard Changelog](references/changelog.md)
- [Official VAT Invoice Verification Platform](https://inv-veri.chinatax.gov.cn)
- [ClawHub Skill Page](https://clawhub.ai/jeffersplind92/skills/tax-invoice-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON-like structured results, Python snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include invoice record fields, deduplication status, verification status, compliance summaries, and Feishu-ready Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
