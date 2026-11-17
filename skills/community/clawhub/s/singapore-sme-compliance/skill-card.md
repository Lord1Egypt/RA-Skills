## Description:

Helps Singapore SMEs automate compliance tasks including GST calculation, PEPPOL invoice validation, tax report generation, and IRAS filing deadline tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redwoo](https://clawhub.ai/user/redwoo)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and their agents use this skill to calculate Singapore GST, check registration and filing requirements, validate PEPPOL invoice readiness, and organize GST F5 preparation tasks.

### Deployment Geography for Use:

Singapore

## Known Risks and Mitigations:

Risk: The skill gives conflicting privacy assurances while showing external financial-data and tax-filing API actions.

Mitigation: Review before installing in production accounting or tax workflows, and prefer the local calculator path for GST arithmetic.

Risk: Real invoice values, turnover, Xero data, bearer tokens, CorpPass tokens, or GST F5 return data could be sent to an unapproved endpoint.

Mitigation: Approve the exact endpoint, token scope, and filing environment before allowing the skill to send sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redwoo/skills/singapore-sme-compliance)
- [IRAS GST registration](https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/gst-registration)
- [IRAS GST filing and payment](https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/filing-and-payment)
- [IMDA InvoiceNow](https://www.imda.gov.sg/infocomm-tech-for-business/boost-your-business/productivity-and-technology/invoicenow)
- [CorpPass](https://www.corppass.gov.sg/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with checklist guidance and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled GST calculator requires bash and bc.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
