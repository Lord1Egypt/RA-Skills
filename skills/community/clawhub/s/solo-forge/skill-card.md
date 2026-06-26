## Description: <br>
Solo Forge is a solo-business assistant for document generation, commercial strategy, and project management from lead generation through payment collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiu-difeng](https://clawhub.ai/user/qiu-difeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo operators and small-business users use this skill to create proposals, contracts, quotes, payment reminders, delivery reports, client records, and business reviews while maintaining local JSON records for clients, deals, and configuration. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change sensitive client, deal, payment, and project-status JSON records through broad natural-language triggers. <br>
Mitigation: Review the skill before installing with real business data, keep JSON files out of shared repositories and unprotected synced folders, and manually confirm proposed writes to deals.json, clients.json, and config.json. <br>
Risk: Payment updates and project status changes may alter business records in ways that affect follow-up, invoicing, and reporting. <br>
Mitigation: Require explicit user confirmation for payment and status updates, keep backups of local JSON records, and audit changes before relying on generated reports. <br>
Risk: Generated contracts, quotations, and business recommendations may be incomplete or unsuitable for a specific transaction. <br>
Mitigation: Have users review all generated documents and consult qualified legal or financial professionals for high-value, regulated, or disputed matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qiu-difeng/solo-forge) <br>
- [README](README.md) <br>
- [Proposal module](references/proposal.md) <br>
- [Contract module](references/contract.md) <br>
- [Quotation module](references/quotation.md) <br>
- [Negotiation module](references/negotiation.md) <br>
- [Tracking module](references/tracking.md) <br>
- [Clients module](references/clients.md) <br>
- [Business review module](references/business-review.md) <br>
- [Delivery module](references/delivery.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown documents and guidance, with optional JSON updates to local client, deal, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON records for clients, deals, and configuration when available; users should confirm business-critical writes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
