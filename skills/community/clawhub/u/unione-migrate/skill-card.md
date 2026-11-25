## Description:

Use when moving email sending to UniOne from another provider — SendGrid, Mailgun, Resend, Postmark — or when the code uses their SDKs, keys or API URLs (@sendgrid/mail, mailgun.js, resend, postmark, …) or their SMTP relays (smtp.sendgrid.net, smtp.mailgun.org, smtp.postmarkapp.com): maps the send calls, SMTP settings and headers, templates, webhook events and suppressions to UniOne.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unione](https://clawhub.ai/user/unione)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to migrate transactional email integrations from SendGrid, Mailgun, Resend, or Postmark to UniOne, including send calls, templates, webhooks, and suppression data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration may transfer suppression data to UniOne.

Mitigation: Review the data transfer and suppression mappings before importing suppression records.

Risk: Some local references were unresolved, leaving parts of the migration guidance incomplete.

Mitigation: Resolve the referenced UniOne setup guidance and check the applicable API details before changing a live sending integration.

## Reference(s):

- [UniOne Web API Reference](https://docs.unione.io/en/web-api-ref)
- [mailgun.md](references/mailgun.md)
- [postmark.md](references/postmark.md)
- [resend.md](references/resend.md)
- [sendgrid.md](references/sendgrid.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Code]

**Output Format:** [Markdown with tables, checklists, and inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Migration mappings and implementation guidance]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
