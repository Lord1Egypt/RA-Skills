## Description:

OpenClaw skill for Twilio APIs: Messaging, WhatsApp, Voice, Conversations, Verify, plus Studio, Lookup, Proxy, Sync, TaskRouter, and Segment/Engage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan Twilio API workflows for messaging, WhatsApp, voice, verification, email, and related communications surfaces. It helps produce workflow plans, method checklists, direct HTTP request guidance, and operational guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twilio and SendGrid API actions can contact real people and incur charges.

Mitigation: Require clear user confirmation before sending messages, emails, OTPs, WhatsApp messages, or placing or ending calls.

Risk: Twilio Auth Tokens, API keys, webhook payloads, and communications metadata can expose credentials or personal information.

Mitigation: Use limited API keys, protect Auth Tokens, validate webhook signatures, avoid logging credentials, and minimize unnecessary PII.

## Reference(s):

- [Twilio API Overview](references/twilio-api-overview.md)
- [Auth and Webhook Validation](references/twilio-auth-and-webhooks.md)
- [Messaging (SMS/MMS)](references/twilio-messaging-sms-mms.md)
- [WhatsApp (Twilio Messaging API)](references/twilio-whatsapp.md)
- [Voice (Calls API)](references/twilio-voice.md)
- [Conversations API](references/twilio-conversations.md)
- [Verify API](references/twilio-verify.md)
- [SendGrid (Email)](references/twilio-sendgrid.md)
- [Studio (Flow Builder)](references/twilio-studio.md)
- [Lookup API](references/twilio-lookup.md)
- [Proxy](references/twilio-proxy.md)
- [Sync](references/twilio-sync.md)
- [TaskRouter](references/twilio-taskrouter.md)
- [Segment / Engage (Twilio)](references/twilio-segment-engage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with workflow plans, checklists, operational guardrails, and inline HTTP or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Twilio credentials, sender identities, webhook URLs, and compliance constraints supplied by the user.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
