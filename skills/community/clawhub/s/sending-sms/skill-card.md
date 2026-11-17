## Description:

Sends SMS messages via the Sendly API with the Node.js SDK or REST API. Handles single messages, batch sends, scheduling, conversations, and sandbox testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendly-live](https://clawhub.ai/user/sendly-live)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send transactional or marketing SMS through Sendly, including single messages, scheduled messages, batch sends, message lookup, and two-way conversation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Sendly API keys can send real SMS messages and incur charges.

Mitigation: Use sk_test_* keys for testing, confirm recipients and message type before live sends, and reserve sk_live_* keys for intentional production use.

Risk: Batch sends can contact many recipients at once.

Mitigation: Review recipient lists and message content before execution, especially for large batches.

Risk: Marketing messages have compliance constraints and misclassifying them as transactional can create legal risk.

Mitigation: Classify messageType correctly and follow quiet-hour and recipient-consent requirements before sending marketing SMS.

## Reference(s):

- [Sending SMS skill page](https://clawhub.ai/sendly-live/skills/sending-sms)
- [Sendly SMS API docs](https://sendly.live/docs/sms)
- [Sendly SDK docs](https://sendly.live/docs/sdks)
- [Sendly OpenAPI spec](https://sendly.live/openapi.yaml)
- [Sendly sandbox docs](https://sendly.live/docs/sandbox)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, Bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes API key configuration, REST requests, Node.js SDK examples, response shapes, sandbox test numbers, and SMS compliance notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
