## Description: <br>
Reads and sends QQ Mail messages using IMAP for mailbox access and SMTP for outbound mail, with guidance for credential setup, message parsing, and common mail filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure QQ Mail access, inspect recent or filtered mailbox contents, parse message text, and send outbound email through QQ Mail with an authorization code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private QQ Mail messages and send real outbound email. <br>
Mitigation: Grant access only to the intended mailbox, keep mail searches narrow, and require explicit user review before sending any email. <br>
Risk: The credential loader uses an inconsistent hard-coded path instead of the documented user-scoped secrets file. <br>
Mitigation: Update the loader to use the documented secrets file or explicit environment variables, and protect the authorization-code file with owner-only permissions. <br>


## Reference(s): <br>
- [QQ Mail IMAP/SMTP authorization help](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256) <br>
- [Sending Email Reference](references/message-sending.md) <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/qq-mail-read-send) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and bash examples, plus plain-text email status or mailbox summaries when used by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QQ Mail credentials through MAIL_USER and MAIL_PASS or the documented user-scoped secrets file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
