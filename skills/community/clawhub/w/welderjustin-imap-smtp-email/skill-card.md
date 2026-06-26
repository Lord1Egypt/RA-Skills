## Description: <br>
Read and send email via IMAP/SMTP, including checking new or unread messages, fetching content, searching mailboxes, marking messages read or unread, downloading attachments, and sending emails with attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welderjustin](https://clawhub.ai/user/welderjustin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect, search, and manage mailbox contents over IMAP and send messages over SMTP from configured email accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read mailbox content and send email as the configured account. <br>
Mitigation: Install only for accounts where agent mailbox access and send permission are acceptable, and review each send action, recipient, body, and attachment before execution. <br>
Risk: Email credentials or authorization codes can expose the mailbox if mishandled. <br>
Mitigation: Use app passwords or provider authorization codes, keep the .env file private, and keep it out of backups and version control. <br>
Risk: Attachment reads and downloads can expose local files or write files outside the intended workspace if directory access is broad. <br>
Mitigation: Keep allowed read and write directories narrow and review attachment paths before allowing file operations. <br>
Risk: Disabling certificate validation can expose email traffic to interception unless the mail server is fully controlled. <br>
Mitigation: Leave certificate validation enabled unless operating against a trusted self-signed server that you control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/welderjustin/welderjustin-imap-smtp-email) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send email through SMTP, read mailbox content through IMAP, and save attachments to configured allowed directories.] <br>

## Skill Version(s): <br>
0.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
