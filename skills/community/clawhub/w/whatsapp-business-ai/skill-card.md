## Description:

Automates WhatsApp conversations for local businesses, including replies, bookings, lead capture, and follow-ups for gyms, restaurants, salons, clinics, and service-based businesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcvanstad](https://clawhub.ai/user/marcvanstad)

### License/Terms of Use:

MIT-0

## Use Case:

Local service businesses use this skill to automate WhatsApp customer conversations, classify intent, generate replies, capture leads, book appointments, and schedule follow-ups. Human operators can monitor status, export leads, view analytics, pause automation, blacklist numbers, and prepare broadcasts.

### Deployment Geography for Use:

South Africa

## Known Risks and Mitigations:

Risk: The webhook starter can expose files, credentials, databases, or logs through a public ngrok tunnel when the intended webhook server is missing.

Mitigation: Use a fixed webhook service that serves only /webhook, rejects unrelated paths, binds locally behind ngrok, and never serves .env files, databases, or logs.

Risk: WhatsApp access tokens and customer data may be mishandled during testing or deployment.

Mitigation: Store tokens outside the web root with restrictive permissions, rotate any test tokens, and review data retention and sharing settings before production use.

Risk: Automated follow-ups, broadcasts, and third-party integrations can contact customers or share data without adequate governance.

Mitigation: Verify customer consent, opt-out handling, retention policy, and third-party sharing controls before enabling follow-ups, broadcasts, calendar sync, Slack, CRM, or payment integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcvanstad/skills/whatsapp-business-ai)
- [Publisher profile](https://clawhub.ai/user/marcvanstad)
- [Meta WhatsApp webhook registration endpoint](https://graph.facebook.com/v18.0/$WHATSAPP_PHONE_NUMBER_ID/subscriptions)
- [Google Calendar OAuth scope](https://www.googleapis.com/auth/calendar)
- [ngrok download documentation](https://ngrok.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, YAML configuration, JSON intent examples, and WhatsApp reply text templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes business-specific templates, follow-up schedules, booking workflow configuration, and operational commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
