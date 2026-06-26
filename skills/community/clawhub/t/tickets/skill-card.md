## Description: <br>
Let your agent shop tickets online with owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent shop for game tickets and other online purchases through CreditClaw with owner approval, spending checks, and payment status polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend real money and its behavior is broader than ticket buying. <br>
Mitigation: Install only when broad CreditClaw shopping and payment capabilities are intended, keep approval mode set to ask for every purchase, and use low spend limits plus narrow merchant and category restrictions. <br>
Risk: CREDITCLAW_API_KEY is a payment credential that could enable unauthorized spending if exposed. <br>
Mitigation: Store the key only in a secure secrets manager or protected environment variable, and never send it to domains other than creditclaw.com. <br>
Risk: Payment links and x402 payments expand the skill beyond purchasing tickets. <br>
Mitigation: Do not enable payment links or x402 payment rails unless those capabilities are explicitly needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jononovo/tickets) <br>
- [Publisher profile](https://clawhub.ai/user/jononovo) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw skill guide](https://creditclaw.com/creditcard/skill.md) <br>
- [Self-hosted card guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [CreditClaw skill metadata](https://creditclaw.com/creditcard/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CREDITCLAW_API_KEY and CreditClaw API endpoints for registration, status checks, spending permissions, purchases, top-up requests, and payment links.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
