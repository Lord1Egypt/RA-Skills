## Description:

Automates WhatsApp Business API customer support for Indian small businesses by classifying messages, sending configured responses, and escalating complex or sensitive issues for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratilsudra](https://clawhub.ai/user/pratilsudra)

### License/Terms of Use:

MIT-0

## Use Case:

External small-business operators and support teams use this skill to handle common WhatsApp customer messages for orders, pricing, hours, bookings, and complaints. It is intended to reduce routine response work while escalating unresolved or higher-risk conversations to the business owner.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: Owner commands can change business responses and expose ticket data without explicit sender authorization.

Mitigation: Configure strict admin sender checks before enabling owner commands, and review commands that list tickets, resolve tickets, update templates, pause responses, or change fees.

Risk: Forwarding full customer conversations and storing ticket memory can expose customer content beyond the original WhatsApp exchange.

Mitigation: Minimize forwarded customer content, define retention and deletion rules for ticket memory, and disclose that WhatsApp messages are processed through Meta and may be escalated to the business owner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pratilsudra/skills/whatsapp-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/pratilsudra)
- [Meta Cloud API messages endpoint](https://graph.facebook.com/v18.0/{WABA_PHONE_NUMBER_ID}/messages)
- [OpenClaw homepage](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and WhatsApp message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WABA_ACCESS_TOKEN and WABA_PHONE_NUMBER_ID environment variables for WhatsApp Business API access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
