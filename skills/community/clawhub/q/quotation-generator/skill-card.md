## Description: <br>
Auto-generate professional PDF proforma invoices with company letterhead, multi-language support, and post-quote tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and export teams use this skill to draft multilingual proforma invoices for B2B deals, route quote drafts for owner approval, and track post-quote follow-up and CRM status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact customers through WhatsApp or update CRM records without clearly bounded confirmation steps. <br>
Mitigation: Require human approval before any message is sent or CRM record is updated, and confirm the customer, quote contents, recipient, and CRM status each time. <br>
Risk: Generated quotes may depend on customer, pricing, WhatsApp, and CRM data that requires appropriate access controls. <br>
Mitigation: Install only where the agent is permitted to access those workflows, and review product terms, pricing, and customer details before approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ipythoning/quotation-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [PDF proforma invoice content, WhatsApp message drafts, and CRM update guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses customer conversation context and product catalog data to prepare quotes, follow-ups, and quote references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
