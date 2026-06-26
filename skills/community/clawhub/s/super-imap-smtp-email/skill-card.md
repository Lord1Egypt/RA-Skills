## Description: <br>
Read, search, and manage email through IMAP, and send email through SMTP with support for multiple accounts and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent check unread mail, fetch and search messages, manage mailbox state, download attachments, and send email through configured IMAP/SMTP accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured mailbox and SMTP accounts expose sensitive email contents and sending authority. <br>
Mitigation: Install only when that access is intended, use app-specific passwords or provider authorization codes, and remove or rotate saved credentials when access is no longer needed. <br>
Risk: Email fetch and search output can expose private message content in retained terminal or agent logs. <br>
Mitigation: Avoid running mailbox commands in contexts where logs are retained or shared. <br>
Risk: Attachment, body-file, and download operations can read from or write to local paths. <br>
Mitigation: Keep ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS narrow and limited to directories needed for the current workflow. <br>
Risk: SMTP sending can disclose information to unintended recipients. <br>
Mitigation: Verify recipients, subject, body, and attachments before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/super-imap-smtp-email) <br>
- [Google Account app passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text and JSON-style command output with Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, configured IMAP/SMTP credentials, and allowlisted read/write directories for local file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence, user changelog, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
