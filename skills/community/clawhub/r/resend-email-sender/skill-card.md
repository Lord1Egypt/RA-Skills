## Description:

Send emails using Resend API. Use when the user needs to send emails without configuring SMTP servers. Supports text and HTML emails, multiple recipients, CC/BCC, and bulk sending. Ideal for notifications, alerts, newsletters, and automated email workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aprilvkuo](https://clawhub.ai/user/aprilvkuo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to send text or HTML email through Resend without configuring SMTP. It supports notification, alert, newsletter, and automated email workflows with single or multiple recipients, CC, and BCC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Resend API key to send live outbound email, including bulk, CC, and BCC messages.

Mitigation: Require explicit user confirmation of recipients and content before sending, especially for bulk, CC, or BCC messages.

Risk: A broadly scoped or exposed Resend API key could allow unintended email sending.

Mitigation: Use a Resend key with the minimum available permissions and review the skill before installation.

Risk: Loading shared .env files can expose unrelated secrets to the skill runtime.

Mitigation: Avoid placing unrelated secrets in the same .env file used for this skill.

## Reference(s):

- [Resend](https://resend.com)
- [Resend Emails API endpoint](https://api.resend.com/emails)
- [ClawHub skill page](https://clawhub.ai/aprilvkuo/skills/resend-email-sender)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill sends live outbound email through the Resend API and returns a success message with the Resend email ID or an error message.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
