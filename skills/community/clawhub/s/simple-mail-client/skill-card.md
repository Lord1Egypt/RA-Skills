## Description: <br>
Send, receive, and manage email through configured IMAP, POP3, and SMTP mail accounts with support for multiple accounts, attachments, message listing, message retrieval, and IMAP status updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wallinex](https://clawhub.ai/user/wallinex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent work with dedicated mailboxes: send messages, list and read mail, inspect attachment metadata, and mark or move IMAP messages. It is best suited to controlled bot or workflow inboxes rather than primary personal or business accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email and move or change mailbox state, giving an agent broad authority over configured accounts. <br>
Mitigation: Use a dedicated low-privilege mailbox or app-specific password, require confirmation for sends and mailbox moves, and set recipient, attachment, and rate limits before autonomous use. <br>
Risk: A configured primary personal or business inbox could expose sensitive messages and credentials to unintended workflows. <br>
Mitigation: Avoid primary inboxes, keep credentials in host-side configuration, and scope accounts to the minimum mailbox privileges needed for the task. <br>
Risk: Dependency or registry tampering could affect a mail-capable skill during installation. <br>
Mitigation: Prefer HTTPS registry sources for dependency resolution and review dependency provenance during deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wallinex/simple-mail-client) <br>
- [Publisher profile](https://clawhub.ai/user/wallinex) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Configuration, Code] <br>
**Output Format:** [Structured handler responses and configuration-backed mail operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return message metadata, message bodies, attachment metadata, send status, and mailbox update status; attachment sending uses base64 content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
