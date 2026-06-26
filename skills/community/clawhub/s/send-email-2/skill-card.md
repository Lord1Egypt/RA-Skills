## Description: <br>
Send emails via SMTP with support for HTML formatting, file attachments, and email templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, developers, and automation agents use this skill to prepare and send SMTP email messages with plain text, HTML or Markdown content, templates, and attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for email credentials, app passwords, or SMTP tokens in chat. <br>
Mitigation: Use only accounts you control, prefer revocable app passwords or SMTP tokens, avoid sharing primary account passwords, and revoke credentials after use when appropriate. <br>
Risk: The skill defaults to a shared sender account when no sender is specified. <br>
Mitigation: Confirm the sender account with the user and prefer user-controlled sender credentials before allowing any email to be sent. <br>
Risk: Incorrect recipients, subjects, message bodies, template paths, or attachments could send unintended or sensitive information. <br>
Mitigation: Confirm the sender, recipient, subject, body, template path, and every attachment before executing the email send command. <br>


## Reference(s): <br>
- [SMTP Server Configurations](references/smtp-servers.md) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>
- [QQ Mail](https://mail.qq.com) <br>
- [163 Mail](https://mail.163.com) <br>
- [126 Mail](https://mail.126.com) <br>
- [SendGrid](https://app.sendgrid.com) <br>
- [Mailgun](https://app.mailgun.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with SMTP configuration details and executable Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a Python SMTP utility that sends email, converts Markdown to HTML, applies templates, and attaches files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
