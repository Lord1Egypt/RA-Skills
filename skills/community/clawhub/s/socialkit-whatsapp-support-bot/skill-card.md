## Description:

Sets up and runs a business-specific support bot on the official WhatsApp Cloud API, answering from an approved knowledge base, handling opt-outs, and handing other requests to a person.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and developers use this skill to set up WhatsApp customer support for approved FAQs, business hours, bookings, and optionally order status. The bot hands unmatched requests to a person.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot may continue messaging people whose opt-out has been recorded.

Mitigation: Enforce STOP until the person explicitly sends START, and verify opt-out state before sending messages.

Risk: Order status may be revealed without confirming that the customer owns the order.

Mitigation: Keep order lookup disabled until customer ownership is verified.

Risk: Credentials and customer information in handoff logs may be exposed or retained longer than needed.

Mitigation: Protect credentials and customer logs, and define a retention period.

## Reference(s):

- [WhatsApp setup guide](references/setup.md)
- [WhatsApp Cloud API getting started](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
- [WhatsApp Platform pricing](https://business.whatsapp.com/products/platform-pricing)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown setup guidance, shell commands, and JSON support knowledge base]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [FAQ replies come from user-approved text; unmatched requests are handed to a person.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
