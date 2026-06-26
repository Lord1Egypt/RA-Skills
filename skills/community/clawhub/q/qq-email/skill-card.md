## Description: <br>
Send and receive emails via QQ Mail SMTP/IMAP for inbox checks, message reading, email sending, HTML email, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chao-NJ-CN](https://clawhub.ai/user/Chao-NJ-CN) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents use this skill to help a configured QQ Mail user send email, list inbox messages, read specific messages, mark messages as read, and handle attachments. It is intended for workflows where email delivery or mailbox review is requested directly by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles QQ Mail credentials and mailbox contents. <br>
Mitigation: Use environment variables or a secret manager instead of storing authorization codes in TOOLS.md, and avoid committing credentials to source control. <br>
Risk: Email sending can disclose content or attachments to unintended recipients. <br>
Mitigation: Confirm recipients, subjects, message content, and attachment paths before running send commands. <br>
Risk: Saved email attachments may be untrusted files. <br>
Mitigation: Avoid saving attachments unless needed, sanitize filenames and output paths, and treat downloaded attachments as untrusted. <br>


## Reference(s): <br>
- [QQ Mail](https://mail.qq.com) <br>
- [ClawHub skill page](https://clawhub.ai/Chao-NJ-CN/qq-email) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Chao-NJ-CN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, json] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and QQ Mail credentials configured through environment variables or TOOLS.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
