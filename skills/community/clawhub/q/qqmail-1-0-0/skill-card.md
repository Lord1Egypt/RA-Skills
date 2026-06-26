## Description: <br>
Manage QQ Mail (QQmail) via IMAP/SMTP so an agent can read, send, search, and list folders for a configured QQ mailbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunyue1977](https://clawhub.ai/user/sunyue1977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users with QQ Mail accounts use this skill to inspect folders, read or search messages, and send email through QQ Mail after configuring a QQ authorization code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real outbound email through the configured QQ Mail account. <br>
Mitigation: Review each recipient, subject, and message body before running send commands. <br>
Risk: Attachments may disclose private files, customer data, credentials, or regulated information. <br>
Mitigation: Confirm every attachment path and file content before sending; avoid attaching sensitive files unless explicitly required. <br>
Risk: QQMAIL_AUTH_CODE is a mailbox credential that enables IMAP/SMTP access. <br>
Mitigation: Keep the authorization code in environment variables or a secret store, and do not paste it into prompts, logs, or generated documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunyue1977/qqmail-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/sunyue1977) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus QQMAIL_USER and QQMAIL_AUTH_CODE environment variables; uses the Python standard library.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
