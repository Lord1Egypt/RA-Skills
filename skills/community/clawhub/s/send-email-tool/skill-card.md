## Description:

Sends plain-text or HTML email through configured SMTP accounts, with support for attachments, CC/BCC, templates, Markdown-to-HTML conversion, and inline local images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyingtimes](https://clawhub.ai/user/flyingtimes)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure SMTP sending and deliver notifications, reports, and automated messages with optional HTML formatting, templates, attachments, CC/BCC recipients, and embedded local images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP credentials may be exposed or weakly protected if a password is passed as an argument or if keyring is unavailable and fallback files are created.

Mitigation: Install keyring before use, use a dedicated SMTP app password, avoid the --password option, do not use the skill on shared machines, and remove ~/.send_email_password and ~/.send_email_username if fallback storage was ever used.

Risk: Outbound emails, attachments, and embedded local images can disclose sensitive content to unintended recipients.

Mitigation: Review recipients, CC/BCC fields, subject, body, attachments, and image paths before sending; test important templates by sending to yourself first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyingtimes/skills/send-email-tool)
- [Usage documentation](artifact/SKILL.md)
- [Examples](artifact/examples/README.md)
- [Template documentation](artifact/templates/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text guidance with inline shell commands; generated emails may be plain text or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local SMTP configuration and credential-store entries, and can send outbound email with attachments and inline images.]

## Skill Version(s):

2.5.0 (source: server release metadata; artifact _meta.json lists 2.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
