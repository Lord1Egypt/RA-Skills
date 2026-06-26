## Description: <br>
Tencent Exmail lets an agent read, search, send, move, and monitor Tencent Exmail messages over SSL-protected IMAP and SMTP, including attachment upload and download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nopassword2000](https://clawhub.ai/user/nopassword2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to automate Tencent Exmail workflows such as checking inboxes, searching messages, sending mail with attachments, downloading attachments, marking or moving messages, and monitoring new mail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, send, modify, and monitor Tencent Exmail messages when configured with account credentials. <br>
Mitigation: Install it only for intended Tencent Exmail accounts, prefer a client-specific authorization code, and limit access to the local environment configuration containing EXMAIL_ADDRESS and EXMAIL_PASSWORD. <br>
Risk: Email-sending actions can send messages to unintended recipients or include unintended attachments. <br>
Mitigation: Verify recipients, subject, body, and attachment paths before running send commands. <br>
Risk: Downloaded attachments and new-mail hook files can contain sensitive mailbox data. <br>
Mitigation: Store downloaded files and hook-file JSON records in protected locations and remove them when no longer needed. <br>
Risk: A background watcher can continue monitoring the mailbox after the immediate task is complete. <br>
Mitigation: Stop the watcher when it is no longer needed and review any hook file it writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nopassword2000/tencent-exmail) <br>
- [Tencent Exmail server configuration](references/server-config.md) <br>
- [Tencent Exmail troubleshooting](references/troubleshooting.md) <br>
- [Tencent Exmail](https://exmail.qq.com) <br>
- [Tencent Exmail Help](https://exmail.qq.com/help) <br>
- [Tencent Exmail Service Center](http://service.exmail.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce mailbox summaries, message details, send confirmations, attachment download paths, and hook-file JSON records for new mail notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
