## Description: <br>
Manage QQ Mail via IMAP/SMTP to read, send with attachments, search by subject, sender, or date, and list folders using Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pdpaer](https://clawhub.ai/user/pdpaer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to manage a QQ mailbox from a local Python command-line helper, including reading recent mail, opening messages, sending messages with optional attachments, searching mail, and listing folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses a QQ mailbox using a QQ Mail authorization code. <br>
Mitigation: Keep QQMAIL_AUTH_CODE private, avoid logging or sharing it, and revoke the authorization code when access is no longer needed. <br>
Risk: The skill can send email and attach local files when directed by an agent. <br>
Mitigation: Require explicit user confirmation of the recipient, subject, body, and every attachment path before sending email. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pdpaer/qqmail) <br>
- [Publisher profile](https://clawhub.ai/user/pdpaer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python 3 standard library; requires QQMAIL_USER and QQMAIL_AUTH_CODE; can read message contents and send email with attachments through QQ Mail IMAP/SMTP.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
