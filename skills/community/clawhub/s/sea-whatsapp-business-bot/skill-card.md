## Description: <br>
AI-powered WhatsApp auto-responder for MY/SG SMEs. Bilingual BM/EN or CN/EN. Handles appointments, FAQ, orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wms2537](https://clawhub.ai/user/wms2537) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External customer-support and operations teams at Malaysia and Singapore SMEs use this skill to draft concise WhatsApp replies, classify customer intent, identify language, and suggest follow-up actions for appointments, FAQs, order status, escalation, and general messages. <br>

### Deployment Geography for Use: <br>
Malaysia and Singapore <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the runnable endpoint appears to charge by user ID before clear consent or WhatsApp bot work is shown. <br>
Mitigation: Require explicit user consent before each charge, log consent and billing events, and document dispute handling before deployment. <br>
Risk: The security evidence advises verifying who controls the hosted Worker before installing. <br>
Mitigation: Confirm publisher and endpoint control through trusted release channels before routing production traffic or billing calls to the Worker. <br>
Risk: The security evidence treats repeated or automated calls as risky until authentication and consent controls are documented. <br>
Mitigation: Use authentication, rate limits, and automation safeguards for any integration that may trigger repeated calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wms2537/sea-whatsapp-business-bot) <br>
- [Publisher profile](https://clawhub.ai/user/wms2537) <br>
- [Hosted respond endpoint](https://sea-whatsapp-business-bot.swmengappdev.workers.dev/respond) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON object with reply, intent, action, and language fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Replies should be concise and preferably under 160 characters when possible.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
