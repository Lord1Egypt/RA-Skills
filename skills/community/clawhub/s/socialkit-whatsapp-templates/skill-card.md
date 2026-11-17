## Description:

Drafts WhatsApp Business message templates (marketing, utility, authentication), validates them, and submits them to Meta for review through the official WhatsApp Cloud API after the user approves. Use when the user needs a WhatsApp template, wants to check template status or quality, or a broadcast needs a template that does not exist yet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business teams use this agent to draft and validate WhatsApp Business message templates, then submit a person-approved draft to Meta for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly scoped or exposed access token could allow unintended WhatsApp Business account actions.

Mitigation: Use a token limited to the intended WhatsApp Business Account and template-management permissions, and store credentials securely outside repositories.

Risk: An unreviewed or changed template could be submitted with unintended wording or category.

Mitigation: Review the exact draft and category, then approve it in the terminal before submission; repeat approval after any change.

Risk: The required socialkit-social-core dependency has separate behavior and risks.

Mitigation: Assess socialkit-social-core separately before use.

## Reference(s):

- [WhatsApp setup and operating guidance](references/setup.md)
- [WhatsApp Cloud API getting started](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
- [WhatsApp message templates overview](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)
- [ClawHub release page](https://clawhub.ai/ahmadhussain0335/skills/socialkit-whatsapp-templates)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON template files, validation reports, and template status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submission follows explicit user approval of the exact draft in an interactive terminal.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
