## Description: <br>
Reads QQ Mail messages over IMAP, including recent-mail lookup, search, filtering, and decoding of common Chinese and Unicode email encodings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZaviWayne](https://clawhub.ai/user/ZaviWayne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent read a configured QQ Mail inbox, retrieve recent messages, search by date or topic, and filter messages by sender, subject, or business context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access mailbox contents when configured with QQ Mail credentials. <br>
Mitigation: Install only for intended QQ Mail access, use a QQ Mail authorization code instead of the account password, and revoke the code when no longer needed. <br>
Risk: Mailbox credentials stored in the configured secrets file could be exposed if file permissions are too broad. <br>
Mitigation: Keep ~/.openclaw/secrets/mail_qq.env private with 600 permissions and do not commit or share authorization codes. <br>
Risk: Broad prompts may cause the agent to read more email than the user intended. <br>
Mitigation: Ask with a clear date range, sender, subject, keyword, or QQ Mail scope before reading or summarizing messages. <br>


## Reference(s): <br>
- [QQ Mail IMAP Help](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256) <br>
- [ClawHub Skill Page](https://clawhub.ai/ZaviWayne/qq-mail-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mailbox search criteria, decoded message summaries, and setup guidance for MAIL_USER, MAIL_PASS, and ~/.openclaw/secrets/mail_qq.env.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
