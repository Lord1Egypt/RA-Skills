## Description:

AI-powered WhatsApp auto-responder for MY/SG SMEs. Bilingual BM/EN or CN/EN. Handles appointments, FAQ, orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wms2537](https://clawhub.ai/user/wms2537)

### License/Terms of Use:


## Use Case:

External users and small businesses in Malaysia and Singapore use this skill to generate concise WhatsApp auto-responder replies, classify customer intent, detect language, and suggest next actions such as booking appointments, checking orders, or transferring to a human.

### Deployment Geography for Use:

Malaysia and Singapore

## Known Risks and Mitigations:

Risk: Per-call SkillPay billing may charge a supplied user identifier through an external Worker.

Mitigation: Before installation, verify caller authentication, duplicate-charge prevention, and authorization controls for the billing endpoint.

Risk: The billing flow sends a user identifier to an external endpoint.

Mitigation: Use only a billing-scoped identifier and avoid personal or reusable account data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wms2537/skills/sea-whatsapp-business-bot)
- [Publisher profile](https://clawhub.ai/user/wms2537)
- [Skill billing endpoint](https://sea-whatsapp-business-bot.swmengappdev.workers.dev/respond)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, guidance]

**Output Format:** [JSON object with reply, intent, action, and language fields; billing calls return JSON status data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies are intended to be concise WhatsApp responses, preferably under 160 characters when possible.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
