## Description: <br>
Simple Email helps an agent receive, search, manage, and send email through standard IMAP and SMTP services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiming-git](https://clawhub.ai/user/shiming-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent check inboxes, search and fetch messages, mark messages read or unread, download attachments, and send text, HTML, or attachment-bearing email through a configured mailbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a configured mailbox, including reading mail, changing read state, sending messages, and handling attachments. <br>
Mitigation: Use app-specific passwords or authorization codes, keep mailbox credentials out of version control, and review outgoing messages, attachment downloads, and read/unread changes before allowing execution. <br>
Risk: Attachment reads and downloads can expose local files or write mailbox content to disk if broad directories are allowed. <br>
Mitigation: Set narrow ALLOWED_READ_DIRS and ALLOWED_WRITE_DIRS values that cover only the directories needed for the task. <br>


## Reference(s): <br>
- [Simple Email on ClawHub](https://clawhub.ai/shiming-git/simple-email) <br>
- [Publisher profile: shiming-git](https://clawhub.ai/user/shiming-git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and environment configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, IMAP credentials, SMTP credentials, and configured read/write directory allowlists.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact package.json declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
