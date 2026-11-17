## Description:

通用 SMTP 邮件发送工具 lets an agent send plain-text or HTML email through SMTP with multiple recipients, attachments, and common provider auto-detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antarctic-penguin971](https://clawhub.ai/user/antarctic-penguin971)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure SMTP credentials and send notification, report, or reminder emails from an agent workflow. It is suited to workflows that need plain text or HTML messages with optional attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP passwords or app passwords may be stored persistently in plaintext in environment variables or HKCU\Environment.

Mitigation: Use app-specific, revocable SMTP credentials; avoid passing passwords on the command line; prefer a credential manager when available.

Risk: The skill can send local attachments to arbitrary recipients.

Mitigation: Verify recipients, destination domains, subject, body, and every attachment path before each send.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antarctic-penguin971/skills/smtp-mail-sender)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can execute SMTP sends via scripts/send_email.py when the agent invokes the bundled script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
