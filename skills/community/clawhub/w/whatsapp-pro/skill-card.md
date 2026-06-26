## Description: <br>
Automated customer support for Indian small businesses using WhatsApp Business API. Categorizes incoming customer messages (orders, complaints, bookings, price queries), auto-responds with configured templates, and flags complex queries for human review. Ideal for coaching institutes, D2C brands, and local service businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratilsudra](https://clawhub.ai/user/pratilsudra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External small-business operators use this agent to automate WhatsApp customer support, classify customer messages, send templated replies, and escalate complaints or complex queries for human review. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: The agent handles customer contact details and WhatsApp Business messaging credentials. <br>
Mitigation: Use a dedicated revocable Meta token, protect WABA_ACCESS_TOKEN and WABA_PHONE_NUMBER_ID, and define how long ticket and contact data is retained. <br>
Risk: Misconfigured escalation or owner commands could expose customer conversations or allow unintended administrative actions. <br>
Mitigation: Verify the owner phone and escalation destination before deployment, and restrict owner-only commands such as template updates, pause/resume, and ticket resolution. <br>
Risk: Automated customer messaging may create privacy or consent concerns for the business using the skill. <br>
Mitigation: Publish a customer privacy notice and deploy the skill only for a business that intentionally automates WhatsApp support. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pratilsudra/whatsapp-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/pratilsudra) <br>
- [Meta Cloud API messages endpoint](https://graph.facebook.com/v18.0/{WABA_PHONE_NUMBER_ID}/messages) <br>
- [Skill homepage](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and WhatsApp message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces customer replies, ticket summaries, owner commands, setup guidance, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
