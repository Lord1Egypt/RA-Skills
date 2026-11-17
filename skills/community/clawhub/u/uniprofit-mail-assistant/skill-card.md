## Description:

Send emails through the UniProfit OpenClaw-compatible API with a user-created `mail_send` API key for already-approved email delivery through a verified UniProfit mail account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieziqing](https://clawhub.ai/user/xieziqing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill when they need an agent to deliver already-approved email content through a verified UniProfit mail account and report the confirmed send status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured UniProfit API base URL receives the mail_send key and email message contents.

Mitigation: Install only with a trusted HTTPS UniProfit API base URL and verify that the environment configuration points to the intended service before use.

Risk: Email delivery is an external action that can expose incorrect recipients, sender accounts, or unapproved content.

Mitigation: Confirm actual delivery intent, sender account, recipient, subject, and final body before sending; report success only after API confirmation.

Risk: Command-line arguments and logs may expose confidential email bodies or credential-adjacent operational details.

Mitigation: Avoid putting confidential content into command lines or logs, and treat UNIPROFIT_MAIL_SEND_KEY as a live credential.

## Reference(s):

- [API Reference](references/api.md)
- [Error Handling](references/error-handling.md)
- [Mail Constraints](references/mail-constraints.md)
- [ClawHub Skill Page](https://clawhub.ai/xieziqing/skills/uniprofit-mail-assistant)
- [Publisher Profile](https://clawhub.ai/user/xieziqing)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional shell command usage and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports recipient, send status, and record or message identifiers when the API confirms delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
