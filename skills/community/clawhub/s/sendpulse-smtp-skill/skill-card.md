## Description:

Send transactional and bulk email through SendPulse using its REST API or SMTP relay, with guidance on setup, troubleshooting, deliverability, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ymaievska-lang](https://clawhub.ai/user/ymaievska-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure SendPulse SMTP and send or troubleshoot transactional emails from applications. It provides REST API and SMTP relay guidance, including sender setup, deliverability, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs permanent deletion of email addresses, which may be difficult to undo.

Mitigation: Prefer reversible suppression unless you explicitly approve a recoverable cleanup.

Risk: The skill suggests disabling an account access restriction without clear safeguards.

Mitigation: Keep IP restrictions enabled and add only the intended sending server.

Risk: Live sends can disclose email content and attachments to SendPulse or unintended recipients.

Mitigation: Use a separate revocable credential and confirm recipients and attachments before live sends; account for SendPulse receiving the email data.

## Reference(s):

- [SendPulse SMTP API documentation](https://sendpulse.com/integrations/api/smtp?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill)
- [SendPulse skill source repository](https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-smtp-skill)
- [API reference](references/api-reference.md)
- [SMTP relay setup](references/smtp-relay.md)
- [Deliverability guidance](references/deliverability.md)
- [Webhook guidance](references/webhooks.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code snippets and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
