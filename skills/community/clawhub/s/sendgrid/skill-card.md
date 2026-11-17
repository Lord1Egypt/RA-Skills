## Description:

Helps agents send SendGrid emails and manage contacts, templates, suppressions, statistics, sender identities, and API keys through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and developers use this skill to send transactional or marketing emails, maintain mailing lists and templates, manage suppressions, and review delivery performance in their authorized SendGrid account. It also provides guidance for user-approved SendGrid automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email actions can deliver messages to real recipients or alter contact and suppression lists.

Mitigation: Before approving writes, confirm the recipient list, sender identity, message content, and intended list changes.

Risk: API keys can grant persistent access to the SendGrid account.

Mitigation: Create keys only on explicit request, verify the required scopes, and delete unused keys when the task is complete.

Risk: Connections, hosted functions, and triggers can continue accessing the account or deliver data to automation destinations.

Mitigation: Confirm the exact connection and each destination before approval; delete unused connections, functions, and triggers afterward.

## Reference(s):

- [ClawHub SendGrid skill](https://clawhub.ai/byungkyu/skills/sendgrid)
- [Maton](https://maton.ai)
- [SendGrid API documentation](https://www.twilio.com/docs/sendgrid/api-reference)
- [SendGrid Mail Send API](https://www.twilio.com/docs/sendgrid/api-reference/mail-send)
- [SendGrid Marketing Contacts API](https://www.twilio.com/docs/sendgrid/api-reference/contacts)
- [Scheduled trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command, API, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and an authorized Maton connection; writes require explicit user approval.]

## Skill Version(s):

1.2.7 (source: server-resolved ClawHub release; skill metadata states 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
