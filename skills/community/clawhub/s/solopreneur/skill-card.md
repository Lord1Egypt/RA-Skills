## Description: <br>
Solopreneur helps solo business owners manage dashboards, pipeline tracking, invoicing, priorities, and weekly reviews while keeping business data local. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo business owners, freelancers, and independent consultants use this skill to organize local client records, pipeline status, invoices, priorities, revenue metrics, and weekly business reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client and financial records are stored locally and may contain sensitive business data. <br>
Mitigation: Keep the local workspace access controlled, use explicit requests for client or financial updates, and manage retention and deletion according to business needs. <br>
Risk: Invoice, pipeline, and priority outputs may be incomplete or unsuitable for accounting, tax, payment, or legal decisions. <br>
Mitigation: Use outputs for organization and drafting only; do not use the skill to process payments, file taxes, or replace accountant or legal counsel review. <br>
Risk: Future helper scripts could change how local business records are read or updated. <br>
Mitigation: Review added helper scripts before relying on them for client, invoice, pipeline, or revenue records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AGIstack/solopreneur) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and terminal text with local JSON-backed business records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local memory records under the solopreneur workspace; no payment processing or cloud accounting integration is described.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
