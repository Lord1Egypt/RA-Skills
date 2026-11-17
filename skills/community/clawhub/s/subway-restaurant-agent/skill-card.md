## Description:

Production-ready WhatsApp ordering agent for restaurants and QSRs that handles natural-language orders, suggests personalized upsells, pulls menus from Google Sheets, logs orders, and uses ThumbGate safety rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant and QSR operators use this agent to accept WhatsApp customer orders, answer menu questions, suggest order add-ons, confirm totals, and log orders to Google Sheets. Installers configure OpenClaw, WhatsApp, Google Sheets, and ThumbGate before deploying it for customer conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer phone numbers, order details, and notes may be stored in Google Sheets.

Mitigation: Restrict the Google Sheet to a least-privilege service account, disclose customer data handling, and avoid collecting phone numbers or free-form notes unless operationally necessary.

Risk: The setup guide asks installers to run an unpinned third-party ThumbGate command.

Mitigation: Use a pinned and reviewed ThumbGate version and test installation in an isolated environment before deploying.

Risk: Security evidence marks the release as suspicious pending careful review.

Mitigation: Review the skill and dependencies before installation, scan the release artifact, and validate customer-facing behavior before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/igorganapolsky/skills/subway-restaurant-agent)
- [Publisher profile](https://clawhub.ai/user/igorganapolsky)
- [ElevenLabs voice provider signup](https://elevenlabs.io/affiliates)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with conversational response guidance and inline setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WhatsApp customer replies, order confirmations, upsell suggestions, and Google Sheets logging instructions during agent operation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
