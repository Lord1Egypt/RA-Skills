## Description: <br>
OpenClaw skill for Twilio APIs: Messaging, WhatsApp, Voice, Conversations, Verify, plus Studio, Lookup, Proxy, Sync, TaskRouter, and Segment/Engage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan Twilio and SendGrid API workflows for messaging, WhatsApp, voice, conversations, verification, email, and related communications services. It emphasizes direct HTTPS requests, webhook validation, credential handling, and operational guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Twilio API keys, Auth Tokens, phone numbers, email addresses, and webhook payloads are sensitive. <br>
Mitigation: Use least-privileged keys, store secrets in a vault, avoid logging credentials or unnecessary personal data, and rotate credentials regularly. <br>
Risk: Outbound messages, emails, calls, or account-affecting requests can create cost, compliance, or user-impacting effects. <br>
Mitigation: Require human confirmation before sending or modifying account state, enforce opt-in and regional compliance, and throttle or retry safely. <br>


## Reference(s): <br>
- [Twilio API Overview](references/twilio-api-overview.md) <br>
- [Auth and Webhook Validation](references/twilio-auth-and-webhooks.md) <br>
- [Messaging (SMS/MMS)](references/twilio-messaging-sms-mms.md) <br>
- [WhatsApp (Twilio Messaging API)](references/twilio-whatsapp.md) <br>
- [Voice (Calls API)](references/twilio-voice.md) <br>
- [Conversations API](references/twilio-conversations.md) <br>
- [Verify API](references/twilio-verify.md) <br>
- [SendGrid (Email)](references/twilio-sendgrid.md) <br>
- [Studio (Flow Builder)](references/twilio-studio.md) <br>
- [Lookup API](references/twilio-lookup.md) <br>
- [Proxy](references/twilio-proxy.md) <br>
- [Sync](references/twilio-sync.md) <br>
- [TaskRouter](references/twilio-taskrouter.md) <br>
- [Segment / Engage (Twilio)](references/twilio-segment-engage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with endpoint, authentication, webhook, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plans and guardrails; it does not execute API calls by itself.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
