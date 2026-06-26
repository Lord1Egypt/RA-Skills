## Description: <br>
Monitors QQ Mail for new messages, provides scheduled checks and spoken notifications, and includes helper scripts for reading and sending mail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksswei](https://clawhub.ai/user/ksswei) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and end users can use this skill to monitor a QQ Mail inbox, receive new-mail alerts, inspect recent messages, and send test email through QQ Mail IMAP/SMTP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private QQ Mail inbox contents and expose message metadata or verification codes. <br>
Mitigation: Use a dedicated revocable QQ Mail authorization code and require explicit user confirmation before reading messages or revealing verification codes. <br>
Risk: Spoken notifications can disclose sender names, subjects, or codes in shared spaces. <br>
Mitigation: Disable or limit TTS where other people may hear notifications. <br>
Risk: The send-mail helper can send email through the configured account. <br>
Mitigation: Require explicit confirmation before sending email and review recipient, subject, and body before execution. <br>
Risk: Recurring checks can continue running after installation. <br>
Mitigation: Verify that any scheduled job can be paused or removed and use a reasonable check interval. <br>


## Reference(s): <br>
- [Qq Mail Monitor on ClawHub](https://clawhub.ai/ksswei/qq-mail-monitor) <br>
- [ksswei publisher profile](https://clawhub.ai/user/ksswei) <br>
- [QQ Mail](https://mail.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python script commands and plain-text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit new-mail status, sender, subject, timestamp, TTS text, and test-send results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, _meta.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
