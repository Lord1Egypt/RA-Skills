## Description:

Automated customer support for Indian small businesses using WhatsApp Business API, classifying customer messages, sending configured auto-responses, and flagging complex queries for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utsavs](https://clawhub.ai/user/utsavs)

### License/Terms of Use:


## Use Case:

External small-business owners in India use this skill to handle WhatsApp customer support for orders, complaints, bookings, price questions, business-hour replies, and owner escalations.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: Owner commands can change templates, fees, tickets, and responder state without enough authorization controls.

Mitigation: Use a dedicated authenticated owner channel or sender allowlist and require confirmation before applying template, fee, ticket, and pause/resume changes.

Risk: Customer phone numbers and full conversations may be stored or forwarded more broadly than necessary.

Mitigation: Add a customer privacy notice and minimize storage or forwarding of raw phone numbers and full conversation text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utsavs/skills/whatsapp-biz-responder)
- [ClawHub homepage](https://clawhub.ai)
- [Meta Cloud API message endpoint](https://graph.facebook.com/v18.0/{WABA_PHONE_NUMBER_ID}/messages)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, API calls]

**Output Format:** [Markdown with JSON configuration examples and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WABA_ACCESS_TOKEN and WABA_PHONE_NUMBER_ID environment variables.]

## Skill Version(s):

1.0.0 (source: evidence release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
