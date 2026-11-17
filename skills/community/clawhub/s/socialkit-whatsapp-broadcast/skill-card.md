## Description:

Sends an approved WhatsApp template to opted-in contacts only through the official WhatsApp Cloud API, after showing recipients, exclusions and an estimated cost and getting the user's approval. Use when the user wants to message a list of customers on WhatsApp, send a WhatsApp campaign, announcement or bulk update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Business teams use this skill to plan and send approved WhatsApp template campaigns to opted-in contacts, reviewing exclusions and estimated costs before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipient selection or rate-card estimate can change after approval.

Mitigation: Preserve the exact approved recipient selection and estimate, and get fresh approval before adding recipients or changing pricing details. Continue honoring new opt-outs.

Risk: Local contact and delivery-result files contain sensitive information.

Mitigation: Protect the local contact and result files from unauthorized access.

## Reference(s):

- [WhatsApp setup guide](references/setup.md)
- [WhatsApp pricing setup](references/pricing.md)
- [WhatsApp Cloud API getting started](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
- [WhatsApp message templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)
- [WhatsApp platform pricing](https://business.whatsapp.com/products/platform-pricing)
- [WhatsApp opt-in guidance](https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON status reports]

**Output Format:** [Markdown guidance, shell commands, CSV and JSON configuration, and JSON plan and send reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plan reports summarize eligible recipients, exclusions and estimated cost; send reports summarize sent, skipped and failed messages.]

## Skill Version(s):

0.3.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
