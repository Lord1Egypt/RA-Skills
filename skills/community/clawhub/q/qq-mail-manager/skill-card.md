## Description: <br>
Manages a configured QQ Mail mailbox by listing folders, searching and reading messages, downloading attachments, marking messages, moving or deleting messages, and sending or replying to email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sccc726](https://clawhub.ai/user/sccc726) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage a QQ Mail account through an agent, including browsing, searching, reading, sending, replying to, moving, deleting, and downloading attachments from email. It is appropriate when the user intends to delegate mailbox management to the agent with configured QQ Mail authorization credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has full delegated access to the configured QQ mailbox, including message contents and attachments. <br>
Mitigation: Use a dedicated QQ Mail authorization code instead of the account password, keep it secret, and revoke it when access is no longer needed. <br>
Risk: The skill can send email and move or delete mailbox messages after confirmation. <br>
Mitigation: Review recipients, message content, and move/delete previews carefully before confirming any action. <br>
Risk: Attachment downloads may place email files on the local filesystem. <br>
Mitigation: Review attachment names and destination paths before downloading, and inspect downloaded files before opening or sharing them. <br>


## Reference(s): <br>
- [QQ Mail configuration guide](references/qq-email-config.md) <br>
- [QQ Mail web login](https://mail.qq.com) <br>
- [ClawHub release page](https://clawhub.ai/sccc726/qq-mail-manager) <br>
- [Publisher profile](https://clawhub.ai/user/sccc726) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown responses with tabular email summaries, JSON script outputs, shell command invocations, and downloaded attachment files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QQ_EMAIL and QQ_EMAIL_AUTH_CODE. Destructive mailbox changes and sending require user preview and confirmation; attachment downloads write files to a selected local directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
