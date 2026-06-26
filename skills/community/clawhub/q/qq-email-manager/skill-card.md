## Description: <br>
QQ Email Manager helps agents manage Tencent Enterprise Mail and compatible IMAP/SMTP mailboxes by listing, reading, searching, sending, replying, forwarding, marking, and summarizing email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangmu-git2](https://clawhub.ai/user/liangmu-git2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to operate a configured email account through agent-issued commands. It is intended for mailbox triage, message search, reading, sending, replying, forwarding, marking messages, listing folders, and mailbox statistics when the user has supplied their own IMAP/SMTP credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and sends email using credentials stored in a local configuration file. <br>
Mitigation: Use an app-specific email password, restrict file permissions on the configuration file, and keep the file out of version control and shared outputs. <br>
Risk: Send, reply, reply-all, and forward commands can transmit messages to recipients chosen by the agent or prompt context. <br>
Mitigation: Require manual review of recipients, subject, message body, reply-all scope, and forward targets before allowing any outbound email command. <br>
Risk: Attachment support can send arbitrary local files when their paths are supplied. <br>
Mitigation: Manually verify every attachment path and only run attachment commands from a workspace that does not expose unrelated sensitive files. <br>
Risk: Read, list, search, folder, and statistics commands expose mailbox metadata and message contents to the agent session. <br>
Mitigation: Use the skill only in sessions where mailbox contents may be processed, and avoid sharing logs or JSON outputs that contain sensitive email data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liangmu-git2/qq-email-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command responses with setup and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local email configuration file containing IMAP/SMTP server settings and account credentials; commands can read mailbox contents, send messages, forward messages, change message flags, and attach local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
