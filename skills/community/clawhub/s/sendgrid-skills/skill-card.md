## Description:

Routes explicit SendGrid email-sending and inbound-parse workflows to focused guides and tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to send transactional email through SendGrid and configure or diagnose SendGrid Inbound Parse workflows. It also provides local payload diagnostics and setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live sends transmit message content and recipient data to SendGrid and recipients, and may incur charges.

Mitigation: Obtain approval for the sender, recipients, exact content, template data, and attachments before sending; minimize personal data.

Risk: Inbound email and webhook content may be private or untrusted, and parser diagnostics can expose message bodies or attachments.

Mitigation: Authenticate inbound receivers, limit and sanitize processing, scan attachments, redact logs, and keep approved diagnostic captures and output private.

Risk: The security scan was partial and only partially interpreted the webhook parser.

Mitigation: Review the skill and its declared tool scope before use, especially for components not covered by the scan.

## Reference(s):

- [SendGrid Documentation](https://docs.sendgrid.com)
- [Mail Send API Reference](https://docs.sendgrid.com/api-reference/mail-send/mail-send)
- [Inbound Parse Webhook Guide](https://docs.sendgrid.com/for-developers/parsing-email/setting-up-the-inbound-parse-webhook)
- [SendGrid Node SDK](https://github.com/sendgrid/sendgrid-nodejs)
- [Single Email Examples](send-email/references/single-email-examples.md)
- [Inbound Webhook Examples](sendgrid-inbound/references/webhook-examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with code examples, shell commands, configuration snippets, and JSON diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on whether the workflow covers sending, inbound setup, or local payload diagnostics.]

## Skill Version(s):

1.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
