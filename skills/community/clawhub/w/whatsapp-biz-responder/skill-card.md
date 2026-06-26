## Description: <br>
Automated customer support for Indian small businesses using WhatsApp Business API. Categorizes incoming customer messages (orders, complaints, bookings, price queries), auto-responds with configured templates, and flags complex queries for human review. Ideal for coaching institutes, D2C brands, and local service businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utsavs](https://clawhub.ai/user/utsavs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External small-business operators use this agent to classify WhatsApp customer messages, send configured replies, escalate complaints or complex requests, and track unresolved tickets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can send WhatsApp messages through a real business account. <br>
Mitigation: Use a dedicated WhatsApp Business token for this automation and review behavior before enabling it for customers. <br>
Risk: Owner commands can change templates, resolve tickets, pause the responder, or expose message statistics. <br>
Mitigation: Restrict owner commands to a verified owner identity or trusted admin channel. <br>
Risk: Ticket memory and escalation messages may contain customer phone numbers and support details. <br>
Mitigation: Notify customers about escalation and retention practices, then minimize, expire, or delete stored ticket data when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utsavs/whatsapp-biz-responder) <br>
- [Meta Cloud API messages endpoint](https://graph.facebook.com/v18.0/{WABA_PHONE_NUMBER_ID}/messages) <br>
- [OpenClaw homepage](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and WhatsApp response templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WABA_ACCESS_TOKEN and WABA_PHONE_NUMBER_ID environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
