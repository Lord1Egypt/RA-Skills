## Description:

SendGrid Skills helps agents send transactional email and receive inbound email programmatically through SendGrid's Mail Send API and Inbound Parse Webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to configure SendGrid workflows, draft integration code, run provided shell utilities, send transactional messages, and handle inbound email webhook payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send live email through a configured SendGrid account.

Mitigation: Use a Mail Send-scoped API key, keep it out of logs, and confirm recipients and content before sending.

Risk: The webhook verifier can test user-provided network endpoints.

Mitigation: Do not run the verifier against untrusted or internal URLs; review the endpoint before execution.

Risk: Inbound email payloads may contain untrusted HTML, attachments, or prompt-injection content.

Mitigation: Require webhook authentication, apply allowlists and size limits, sanitize HTML, scan attachments, and filter content before passing it to AI systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vince-winkintel/skills/sendgrid-skills)
- [SendGrid documentation](https://docs.sendgrid.com)
- [Mail Send API reference](https://docs.sendgrid.com/api-reference/mail-send/mail-send)
- [Inbound Parse Webhook](https://docs.sendgrid.com/for-developers/parsing-email/setting-up-the-inbound-parse-webhook)
- [SendGrid Node SDK](https://github.com/sendgrid/sendgrid-nodejs)
- [Send Email Best Practices](send-email/references/best-practices.md)
- [SendGrid SDK Installation](send-email/references/installation.md)
- [Single Email Examples](send-email/references/single-email-examples.md)
- [Inbound Parse Best Practices](sendgrid-inbound/references/best-practices.md)
- [Inbound Parse Webhook Examples](sendgrid-inbound/references/webhook-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, JSON examples, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENDGRID_API_KEY and the curl, jq, and node binaries for bundled scripts.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
