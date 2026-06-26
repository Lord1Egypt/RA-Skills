## Description: <br>
A ThumbGate-hardened WhatsApp ordering agent for QSRs, featuring smart upsells and inventory awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant operators and QSR teams use this skill to run WhatsApp-based order capture, upsell prompts, inventory checks, order validation, and Google Sheets order logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WhatsApp API tokens and Google Sheets credentials could expose ordering systems or customer data if reused or stored unsafely. <br>
Mitigation: Install with a dedicated WhatsApp token and a least-privilege Google Sheet or service account, keep .env out of source control, and test first with sandbox credentials. <br>
Risk: Order logs can contain customer identifiers, order details, totals, timestamps, and allergy notes. <br>
Mitigation: Restrict sheet and file access and provide a customer-facing privacy notice that explains what order data is stored. <br>
Risk: Incorrect inventory, allergen, price, or duplicate-order handling could create customer safety or transaction issues. <br>
Mitigation: Review and enforce the provided ThumbGate rules before production use, especially inventory checks, allergen confirmation, price matching, duplicate-order checks, and PII logging controls. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/igorganapolsky/subway-whatsapp-ordering) <br>
- [Setup Guide](artifact/setup-guide.md) <br>
- [ThumbGate Prevention Rules](artifact/thumbgate-rules.md) <br>
- [Premium Revenue Machine bundle](https://iganapolsky.gumroad.com/l/gvpllr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and structured ordering rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent output may include order summaries, upsell prompts, validation checks, pickup estimates, and Google Sheets logging guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
