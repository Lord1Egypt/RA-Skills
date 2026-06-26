## Description: <br>
Helps Singapore SMEs with GST calculations, GST registration checks, GST F5 preparation, PEPPOL invoice validation, and IRAS filing deadline tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redwoo](https://clawhub.ai/user/redwoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users, accountants, and advisors supporting Singapore SMEs use this skill to calculate GST, prepare compliance checklists, draft GST F5 summaries, validate PEPPOL invoice requirements, and track filing deadlines. <br>

### Deployment Geography for Use: <br>
Singapore <br>

## Known Risks and Mitigations: <br>
Risk: External API examples and accounting or filing integrations may expose sensitive invoice, tax, Xero, QuickBooks, CorpPass, or IRAS data. <br>
Mitigation: Do not provide production credentials or submit business data externally unless the endpoint, payload, and user approval have been verified. <br>
Risk: Tax and compliance guidance may be incomplete or stale for a specific filing obligation. <br>
Mitigation: Validate filing decisions, deadlines, and GST calculations against official IRAS guidance or a qualified advisor before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redwoo/singapore-sme-compliance) <br>
- [IRAS GST registration](https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/gst-registration) <br>
- [IRAS GST filing and payment](https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/filing-and-payment) <br>
- [IMDA InvoiceNow](https://www.imda.gov.sg/infocomm-tech-for-business/boost-your-business/productivity-and-technology/invoicenow) <br>
- [CorpPass](https://www.corppass.gov.sg/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local calculator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and bc for the bundled GST calculator; external API examples require endpoint and payload review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
