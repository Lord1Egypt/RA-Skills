## Description: <br>
Configures an SMTP sender and sends plain-text or HTML email with attachments, CC/BCC, templates, Markdown conversion, and inline images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyingtimes](https://clawhub.ai/user/flyingtimes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to send notification, report, and automation emails from an agent workflow after configuring SMTP credentials and sender settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has SMTP sending authority and can send messages to external recipients. <br>
Mitigation: Install only when that authority is intended, and review recipients, CC, BCC, subject, and body before sending. <br>
Risk: If keyring is unavailable, credentials may be persisted in local base64-encoded fallback files. <br>
Mitigation: Use a dedicated app password, verify keyring works before saving credentials, and avoid or delete ~/.send_email_password and ~/.send_email_username. <br>
Risk: Attachments and inline images can email local files or images externally, including from automated or scheduled workflows. <br>
Mitigation: Review attachment paths, Markdown image paths, and inline-image paths before sending, especially when using automation or cron. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Markdown, HTML] <br>
**Output Format:** [Markdown guidance with bash commands; email content may be plain text, Markdown-derived HTML, or templated HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send attachments, inline local images, CC, and BCC through SMTP.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
