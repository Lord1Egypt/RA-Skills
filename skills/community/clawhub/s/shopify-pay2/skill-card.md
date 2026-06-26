## Description: <br>
Guides an agent through CreditClaw-backed shopping, checkout, wallet, webhook, and sales-management workflows across Shopify and other merchants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to set up CreditClaw access, find products, request owner-approved spending, complete merchant checkout, and manage related payment or sales workflows. It is intended for agents that are explicitly authorized to spend money and handle checkout operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This is high-impact payment automation that can spend money across many merchants and manage checkout, webhook, and sales workflows. <br>
Mitigation: Install only when that authority is intentional; use a dedicated low-limit wallet or card and keep approval_mode set to ask_for_everything unless a human owner explicitly changes it. <br>
Risk: The skill handles sensitive payment data and a CreditClaw API key that can authorize spending. <br>
Mitigation: Store credentials only in a secure secrets manager, never place raw card data or API keys in prompts or logs, and send the CreditClaw API key only to creditclaw.com. <br>
Risk: Broad merchant access and webhook callback changes can route spending or payment events outside the intended scope. <br>
Mitigation: Restrict merchant and domain permissions, review callback_url changes before use, and monitor the owner dashboard for purchase attempts and account activity. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TripleHippo/shopify-pay2) <br>
- [CreditClaw Homepage](https://creditclaw.com) <br>
- [CreditClaw API Base](https://creditclaw.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with bash commands, API request examples, JSON examples, and platform-specific checkout guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and produces operational instructions for payment, checkout, webhook, wallet, and sales-management tasks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
