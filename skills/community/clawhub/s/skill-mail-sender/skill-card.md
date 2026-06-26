## Description: <br>
Sends email through SMTP in HTML or Markdown format, including batch messages, notifications, reports, and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weznai](https://clawhub.ai/user/weznai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to send formatted emails, reports, reminders, and batch notifications through configured SMTP credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real email messages using SMTP credentials. <br>
Mitigation: Review recipients, subject, and body before important or bulk sends, and use a dedicated mailbox or app password. <br>
Risk: Mailbox credentials may be stored in configuration files or environment variables. <br>
Mitigation: Protect config files with restrictive permissions, avoid committing config or .env files, and prefer app-specific authorization codes. <br>
Risk: Unpinned Python dependencies may change behavior over time. <br>
Mitigation: Pin and review dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Mail Sender Release](https://clawhub.ai/weznai/skill-mail-sender) <br>
- [Configuration Guide](references/config.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [HTML or Markdown email content, Python code snippets, shell commands, configuration JSON, and JSON-like Python result dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can address one or multiple recipients and returns success status, message text, and failed recipient details.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
